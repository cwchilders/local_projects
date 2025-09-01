import argparse
from bs4 import BeautifulSoup
import real_estate_config as config
import zillow_file_manager as file_manager
import os

# --- Mandatory first step for any script in this project ---
# Call the function to ensure configurations are loaded.
# This makes the dependency explicit.
config.ensure_config()

def extract_image_src(html_content):
    """
    Extracts the image source URL from the provided HTML snippet.
    
    Args:
        html_content (str): A string containing the HTML to parse.
        
    Returns:
        str: The URL of the image, or None if not found.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Find the <li> tag with the specific class
    list_item = soup.find('li', class_='media-stream-tile')
    
    if list_item:
        # Inside the <li>, find the <img> tag
        img_tag = list_item.find('img')
        
        if img_tag:
            # Get the value of the 'src' attribute
            return img_tag.get('src')
            
    return None


def extract_address_from_html(html_content):
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'lxml')

    # Find the button element by checking if its class contains the "StyledTextButton" substring
    address_button = soup.find('button', class_=lambda c: c and 'StyledTextButton' in c)

    # Check if the element was found and extract the text
    if address_button:
        address_text = address_button.get_text(strip=True, separator=' ')
        address_filename = file_manager.sanitize_filename(address_text)
        print(address_filename)
        return address_filename
    else:
        print("Address element not found.")
    return None


# function to extract the largest image URL from a srcset attribute
# This function is used to process gallery images with multiple resolutions
def get_largest_imageURL_from_srcset(srcset_string):
    """
    Extracts the URL of the largest image from a srcset string.
    The largest image is determined by the largest width value (e.g., '1536w').
    """
    largest_url = ""
    max_width = 0

    # Split the srcset string into individual image-width pairs
    image_pairs = srcset_string.split(', ')

    for pair in image_pairs:
        parts = pair.split(' ')
        if len(parts) == 2:
            url = parts[0]
            width_str = parts[1]

            # Extract the numerical width and convert to an integer
            if width_str.endswith('w'):
                try:
                    width = int(width_str[:-1])
                    if width > max_width:
                        max_width = width
                        largest_url = url
                except ValueError:
                    continue
    return largest_url

def extract_images_from_gallery(html_content):
    # Parse the HTML using BeautifulSoup with the lxml parser
    soup = BeautifulSoup(html_content, 'lxml')

    # Find all <source> tags with the type attribute set to "image/jpeg"
    source_tags = soup.find_all('source', {'type': 'image/jpeg'})

    # List to store the largest image URL for each srcset
    largest_urls = []

    # Iterate through each <source> tag and extract the largest URL
    for tag in source_tags:
        srcset_value = tag.get('srcset')
        if srcset_value:
            largest_url = get_largest_imageURL_from_srcset(srcset_value)
            if largest_url:
                largest_urls.append(largest_url)

    # Print the extracted URLs
    print(largest_urls)
    return largest_urls

def download_image(image_url, save_path):
    """
    Downloads an image from the specified URL and saves it to the given path.
    
    Args:
        image_url (str): The URL of the image to download.
        save_path (str): The file path where the image will be saved.
    """
    import requests
    
    response = requests.get(image_url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {save_path}")
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")

def process_image_gallery_files(scrapes_dir=config.scrapes_dir, 
                                download=False, 
                                output_dir=config.output_folder):
    """
    Processes all image gallery HTML snippets in the folder to extract and optionally download images.
    
    Args:
        scrapes_dir (str): The folder with HTML scrapes of the image galleries.
        download (bool): Whether to download the images.
        output_dir (str): The directory to save downloaded images if download is True.
    """
    if not os.path.exists(scrapes_dir):
        print(f"Scrapes directory does not exist: {scrapes_dir}")
        return None
    
    html_files = [filepath for filepath in os.listdir(scrapes_dir)]
    for filename in html_files:
        with open(os.path.join(scrapes_dir, filename), 'r') as file:
            html_content = file.read()
            image_urls = extract_images_from_gallery(html_content)  
            address_filename = extract_address_from_html(html_content)

        if download and output_dir:
            images_folder = os.path.join(output_dir, address_filename if address_filename else "unknown_property")
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
            
            for idx, url in enumerate(image_urls):
                file_extension = os.path.splitext(url)[1]
                save_path = os.path.join(images_folder, f"image_{idx + 1}{file_extension}")
                download_image(url, save_path)
                print(f"Downloaded image to: {save_path}")
        
            print(f"Extracted Image URLs: {image_urls}")

    return image_urls if image_urls else None


# --- Example Usage ---
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract and download images from HTML snippets.")
    parser.add_argument('--scraped_files_dir', default= os.getenv('RE_DEFAULT_FOLDER_IMAGE_SCRAPES'),type=str, help='Dir with html content to parse for images extraction.')
    parser.add_argument('--download', action='store_true', help='Flag to download the extracted image.')
    parser.add_argument('--output', default= os.getenv('RE_DEFAULT_FOLDER_TEST'), type=str, help='Output path to save the downloaded image.')
    
    args = parser.parse_args()
    
    img_urls = process_image_gallery_files(args.scraped_files_dir, args.download, args.output)
    print(f"process_image_gallery_files returned: {img_urls}")
    
