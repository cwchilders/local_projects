import os
import sys
import argparse
from playwright_stealth import Stealth
from playwright.sync_api import sync_playwright
import parse_zillow_page as zillow_page
import zillow_property_manager as property_manager


def scrape_zillow(zillow_url):
    """Scrapes html content for a single Zillow listing.
        
    Args:
        zillow_url (str): The URL for the page.

    Returns:
        content: the raw html string, or None if an Exception is thrown.
    
    """
    
    try:
        print(f"Scraping {zillow_url}...")
        
        with Stealth().use_sync(sync_playwright()) as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(zillow_url)
            
            # Check for CAPTCHA page content, which indicates a bot block.
            if "Press & Hold to confirm you are" in page.content():
                print("CAPTCHA detected. Cannot proceed.")
                return None
            # --- End CAPTCHA check ---

            # --- New: Add a wait to ensure the page is fully loaded ---
            # Wait for the page by waiting for a known element to load.
            # Use a try-except block to handle cases where the element doesn't exist.
            try:
                page.wait_for_selector("dl[class*='StyledOverviewStats']", timeout=10000)
            except Exception:
                print(f" - Stats element not found within timeout for {zillow_url}.")
                return None

            # Get the page content after the element has loaded
            content = page.content()

            # --- Add this section to dump the content to a file ---
            # with open("page_content.html", "w") as f:
            #     f.write(content)
            # print("Successfully dumped page content to 'page_content.html'")
            # --- End of added section ---
       
        return content

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the default filename
    default_filename = 'zillow_listing_urls.txt'

    # Construct the full default file path
    default_file_path = os.path.join(script_dir, default_filename)

    """Main function to handle command-line arguments and run the scraper."""
    parser = argparse.ArgumentParser(description='Scrape Zillow listing stats.')
   # Add the 'url_file' argument with the absolute default path
    parser.add_argument('url_file', 
                    nargs='?', 
                    default=default_file_path,
                    help=f'Path to a text file containing Zillow URLs, one per line. Defaults to "{default_file_path}" if not provided.')
    args = parser.parse_args()
    
    print('Scrape Zillow listing stats')

    try:
        with open(args.url_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file {args.url_file} was not found.")
        sys.exit(1)

    print(f"\nListings to scrape from {args.url_file:}")

    for url in urls:
        content = scrape_zillow(url)
        stats = zillow_page.parse_zillow_stats(content)
        facts = zillow_page.parse_zillow_facts(content)

        name = property_manager.get_property_name(url)
        print(f"\nProperty: {name}")
        id = property_manager.get_property_id_from_url(url)
        print(f"Zillow Property ID: {id}")


        if stats:
            print(f"Stats for {url}:")
            for key, value in stats.items():
                print(f"  - {key.replace('_', ' ').capitalize()}: {value}")
        else:
            print(f"No stats retrieved for {url}.")

        if facts:
            formatted_description = zillow_page.format_zillow_data(facts)
            print(formatted_description)
        else:
            print(f"No facts retrieved for {url}.")

if __name__ == "__main__":
    main()