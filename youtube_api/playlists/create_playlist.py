#!/usr/bin/env python3
"""
YouTube Playlist Creator
Version: 2.0.0
Date: 2024-09-23

Reads song titles from song_list.txt and searches YouTube for each song,
returning top(n) results for each title. Creates actual YouTube playlists.

Features:
- Parses playlist metadata from song_list.txt ([playlist=title] [description=desc])
- Searches YouTube for each song
- Creates YouTube playlist with top results
- Exports search results to JSON

Requirements:
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2

Changelog:
v2.0.0 - Added playlist metadata parsing and actual playlist creation
v1.0.0 - Initial version with search functionality
"""

import os
import json
import re
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# YouTube API settings
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

class YouTubePlaylistCreator:
    def __init__(self, client_secrets_file: str, max_results_per_song: int = 5):
        """
        Initialize YouTube API client

        Args:
            client_secrets_file: Path to OAuth client secrets JSON file
            max_results_per_song: Maximum search results to return per song
        """
        self.client_secrets_file = client_secrets_file
        self.max_results_per_song = max_results_per_song
        self.youtube = None
        self.credentials = None

    def authenticate(self):
        """Authenticate with YouTube API using OAuth2"""
        creds = None
        token_file = 'token.json'

        try:
            # Check if token file exists
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)

            # If there are no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    print("🔄 Refreshing expired credentials...")
                    creds.refresh(Request())
                else:
                    print("🔐 Starting OAuth authentication flow...")
                    print("📝 If you get a 500 error, check:")
                    print("   1. OAuth consent screen is configured")
                    print("   2. Your email is added as a test user (if app is in Testing mode)")
                    print("   3. YouTube Data API v3 is enabled")

                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file, SCOPES)
                    creds = flow.run_local_server(port=0)

                # Save credentials for next run
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())

            self.credentials = creds
            self.youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
            print("✅ Successfully authenticated with YouTube API")

        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            print("💡 Common solutions:")
            print("   1. Check Google Cloud Console OAuth settings")
            print("   2. Add your email as a test user if app is in Testing mode")
            print("   3. Ensure YouTube Data API v3 is enabled")
            print("   4. Try deleting token.json and re-authenticating")
            raise

    def parse_song_list(self, file_path: str) -> tuple[Dict[str, str], List[Dict[str, str]]]:
        """
        Parse song_list.txt file to extract playlist metadata and song titles

        Expected format:
        [playlist=Title]
        [description=Description]
        "Song Title" Artist Name

        Args:
            file_path: Path to song_list.txt file

        Returns:
            Tuple of (playlist_metadata, songs_list)
        """
        songs = []
        playlist_metadata = {
            'title': 'My YouTube Playlist',
            'description': 'Created with YouTube Playlist Creator'
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()

                    # Skip empty lines
                    if not line:
                        continue

                    # Parse playlist metadata
                    playlist_match = re.match(r'\[playlist=(.+)\]', line)
                    if playlist_match:
                        playlist_metadata['title'] = playlist_match.group(1).strip()
                        print(f"📋 Playlist title: {playlist_metadata['title']}")
                        continue

                    description_match = re.match(r'\[description=(.+)\]', line)
                    if description_match:
                        playlist_metadata['description'] = description_match.group(1).strip()
                        print(f"📄 Playlist description: {playlist_metadata['description']}")
                        continue

                    # Skip lines that don't contain quoted titles
                    if '"' not in line:
                        continue

                    # Parse quoted title and artist
                    # Pattern: "Title" Artist
                    match = re.match(r'"([^"]+)"\s+(.+)', line)
                    if match:
                        title = match.group(1).strip()
                        artist = match.group(2).strip()
                        search_query = f"{title} {artist}"

                        songs.append({
                            'title': title,
                            'artist': artist,
                            'search_query': search_query,
                            'line_number': line_num
                        })
                        print(f"📝 Parsed: '{title}' by {artist}")
                    else:
                        print(f"⚠️  Skipping line {line_num}: {line}")

        except FileNotFoundError:
            print(f"❌ Error: Could not find file {file_path}")
            return playlist_metadata, []
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return playlist_metadata, []

        print(f"✅ Parsed {len(songs)} songs from {file_path}")
        return playlist_metadata, songs

    def search_youtube(self, query: str) -> List[Dict[str, str]]:
        """
        Search YouTube for videos matching the query

        Args:
            query: Search query string

        Returns:
            List of video results with title, video_id, channel, etc.
        """
        try:
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=self.max_results_per_song,
                type='video',
                order='relevance'
            ).execute()

            results = []
            for item in search_response['items']:
                video_data = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description'][:100] + '...',
                    'published': item['snippet']['publishedAt'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                results.append(video_data)

            return results

        except Exception as e:
            print(f"❌ Error searching for '{query}': {e}")
            return []

    def create_playlist(self, playlist_title: str, playlist_description: str = "") -> Optional[str]:
        """
        Create a new YouTube playlist

        Args:
            playlist_title: Title for the new playlist
            playlist_description: Description for the playlist

        Returns:
            Playlist ID if successful, None otherwise
        """
        try:
            playlist_response = self.youtube.playlists().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': playlist_title,
                        'description': playlist_description
                    },
                    'status': {
                        'privacyStatus': 'private'  # Change to 'public' if desired
                    }
                }
            ).execute()

            playlist_id = playlist_response['id']
            print(f"✅ Created playlist: {playlist_title} (ID: {playlist_id})")
            return playlist_id

        except Exception as e:
            error_str = str(e)
            if 'youtubeSignupRequired' in error_str:
                print(f"❌ YouTube channel required!")
                print("💡 To fix this:")
                print("   1. Go to https://youtube.com")
                print("   2. Sign in with your Google account")
                print("   3. Create a YouTube channel")
                print("   4. Run this script again")
            else:
                print(f"❌ Error creating playlist: {e}")
            return None

    def add_video_to_playlist(self, playlist_id: str, video_id: str) -> bool:
        """
        Add a video to a YouTube playlist

        Args:
            playlist_id: ID of the playlist
            video_id: ID of the video to add

        Returns:
            True if successful, False otherwise
        """
        try:
            self.youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()
            return True

        except Exception as e:
            print(f"❌ Error adding video {video_id} to playlist: {e}")
            return False

    def process_songs(self, song_list_file: str, output_file: str = 'search_results.json', create_playlist: bool = True):
        """
        Main processing function: read songs, search YouTube, optionally create playlist

        Args:
            song_list_file: Path to song_list.txt file
            output_file: Path to save JSON results
            create_playlist: Whether to create an actual YouTube playlist
        """
        if not self.youtube:
            print("❌ Not authenticated. Call authenticate() first.")
            return

        # Parse songs and metadata from file
        playlist_metadata, songs = self.parse_song_list(song_list_file)
        if not songs:
            print("❌ No songs found to process")
            return

        all_results = []
        playlist_videos = []  # Store video IDs for playlist creation

        # Search for each song
        for i, song in enumerate(songs, 1):
            print(f"\n🔍 Searching {i}/{len(songs)}: {song['search_query']}")

            search_results = self.search_youtube(song['search_query'])

            song_result = {
                'song_info': song,
                'search_results': search_results,
                'result_count': len(search_results)
            }
            all_results.append(song_result)

            # Display top result and add to playlist
            if search_results:
                top_result = search_results[0]
                print(f"   🎵 Top result: {top_result['title']} by {top_result['channel']}")
                playlist_videos.append({
                    'video_id': top_result['video_id'],
                    'title': top_result['title'],
                    'channel': top_result['channel'],
                    'original_query': song['search_query']
                })
            else:
                print(f"   ❌ No results found")

        # Save results to JSON file
        try:
            final_results = {
                'playlist_metadata': playlist_metadata,
                'search_results': all_results,
                'playlist_videos': playlist_videos
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(final_results, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Saved all results to {output_file}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")

        # Create YouTube playlist if requested
        playlist_id = None
        if create_playlist and playlist_videos:
            print(f"\n🎵 Creating YouTube playlist: '{playlist_metadata['title']}'")
            playlist_id = self.create_playlist(
                playlist_metadata['title'],
                playlist_metadata['description']
            )

            if playlist_id:
                print(f"📝 Adding {len(playlist_videos)} videos to playlist...")
                added_count = 0
                for video in playlist_videos:
                    if self.add_video_to_playlist(playlist_id, video['video_id']):
                        added_count += 1
                        print(f"   ✅ Added: {video['title']}")
                    else:
                        print(f"   ❌ Failed to add: {video['title']}")

                print(f"\n🎉 Playlist created! Added {added_count}/{len(playlist_videos)} videos")
                print(f"🔗 Playlist URL: https://www.youtube.com/playlist?list={playlist_id}")

        # Print summary
        total_results = sum(result['result_count'] for result in all_results)
        print(f"\n📊 Summary:")
        print(f"   Songs processed: {len(songs)}")
        print(f"   Total results found: {total_results}")
        print(f"   Average results per song: {total_results/len(songs):.1f}")
        if playlist_id:
            print(f"   Playlist created: {playlist_metadata['title']} (ID: {playlist_id})")

def main():
    """Main execution function"""

    # Configuration
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CLIENT_SECRETS_FILE = os.path.join(SCRIPT_DIR, 'client_secret_782450181754-8tarmea4lrhit1en2gmvhoe9b37jd7d7.apps.googleusercontent.com.json')
    SONG_LIST_FILE = os.path.join(SCRIPT_DIR, 'song_list.txt')
    OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'search_results.json')
    MAX_RESULTS_PER_SONG = 5

    print("🎵 YouTube Playlist Creator")
    print("=" * 50)

    # Check if required files exist
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"❌ Client secrets file not found: {CLIENT_SECRETS_FILE}")
        return

    if not os.path.exists(SONG_LIST_FILE):
        print(f"❌ Song list file not found: {SONG_LIST_FILE}")
        return

    # Initialize and run
    creator = YouTubePlaylistCreator(CLIENT_SECRETS_FILE, MAX_RESULTS_PER_SONG)

    try:
        # Authenticate with YouTube API
        creator.authenticate()

        # Process songs and search YouTube
        creator.process_songs(SONG_LIST_FILE, OUTPUT_FILE)

        print("\n✅ Processing complete!")

    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()