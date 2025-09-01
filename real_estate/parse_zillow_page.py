#!/usr/bin/env python3

from pathlib import Path
from bs4 import BeautifulSoup
import re
import os
import argparse
import sys
import zillow_property_manager as property_manager
from zillow_image_manager import extract_image_src
from zillow_file_manager import property_address_from_filename, save_file_lines
from google_api import get_formatted_address


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Define the default scrape folder
default_scrapes = 'page_scrapes'
# Construct the full default file path
default_scrapes_path = os.path.join(script_dir, default_scrapes)


def parse_zillow_stats(html_content):
    """
    Parses Zillow stats from an HTML string using BeautifulSoup and regex.

    Args:
        html_content (str): The HTML snippet containing the stats.

    Returns:
        dict: A dictionary with the parsed stats, or None if the element is not found.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Use a regex to find the main <dl> element with 'StyledOverviewStats' in its class name.
    stats_dl_regex = re.compile(r'StyledOverviewStats')
    stats_dl = soup.find('dl', class_=stats_dl_regex)

    if not stats_dl:
        return None
    
    # Find all <strong> tags within the <dl> element.
    strong_tags = stats_dl.find_all('strong')
    
    if len(strong_tags) < 3:
        return None
    
    # Extract the data based on the order of the <strong> tags.
    # The regex `[^\d]` removes any non-digit character, including commas.
    
    days_on_zillow_str = re.sub(r'[^\d]', '', strong_tags[0].get_text(strip=True))
    views_str = re.sub(r'[^\d]', '', strong_tags[1].get_text(strip=True))
    saves_str = re.sub(r'[^\d]', '', strong_tags[2].get_text(strip=True))
    
    stats = {
        'days_on_zillow': int(days_on_zillow_str),
        'views': int(views_str),
        'saves': int(saves_str)
    }
    
    return stats

# # --- Example Usage ---
# html_snippet = """
# <dl class="styles__StyledOverviewStats-fshdp-8-111-1__sc-1x11gd9-0 kpgmGL">
# 	<dt><strong>204 days</strong></dt>
# 	<dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp">on Zillow</dt>
# 	<span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
# 	<dt><strong>1,188</strong></dt>
# 	<dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp"><button type="button" aria-expanded="false" aria-haspopup="false" class="TriggerText-c11n-8-111-1__sc-d96jze-0 hAKmPK TooltipPopper-c11n-8-111-1__sc-1v2hxhd-0 isapNu">views</button></dt>
# 	<span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
# 	<dt><strong>61</strong></dt>
# 	<dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp"><button type="button" aria-expanded="false" aria-haspopup="false" class="TriggerText-c11n-8-111-1__sc-d96jze-0 hAKmPK TooltipPopper-c11n-8-111-1__sc-1v2hxhd-0 isapNu">saves</button></dt>
# 	<span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
# </dl>
# """

# zillow_stats = parse_zillow_stats(html_snippet)

# if zillow_stats:
#     print(f"Days on Zillow: {zillow_stats['days_on_zillow']}")
#     print(f"Views: {zillow_stats['views']}")
#     print(f"Saves: {zillow_stats['saves']}")
# else:
#     print("Could not parse Zillow stats from the HTML.")


def parse_zillow_facts(html_content):
    """
    Parses Zillow facts from an HTML string using BeautifulSoup.

    Args:
        html_content (str): The HTML snippet containing the facts.

    Returns:
        dict: A nested dictionary with the parsed facts.
    """
    soup = BeautifulSoup(html_content, 'lxml')

    data = {}
    for category_group in soup.find_all('div', {'data-testid': 'category-group'}):
        group_title = category_group.find('h3', class_=lambda x: x and 'StyledCategoryGroupHeading' in x).get_text(strip=True)
        data[group_title] = {}
        for fact_category in category_group.find_all('div', {'data-testid': 'fact-category'}):
            category_title_tag = fact_category.find('h6', class_=lambda x: x and 'StyledHeading' in x)
            category_title = category_title_tag.get_text(strip=True) if category_title_tag else 'Miscellaneous'
            data[group_title][category_title] = [li.get_text(strip=True) for li in fact_category.find_all('li')]

    # print(data)
    return data

def format_zillow_data(zillow_data):
    """
    Formats Zillow data from a dictionary into a Markdown string.

    Args:
        zillow_data (dict): The dictionary containing property facts and features.

    Returns:
        str: A Markdown-formatted string of the property data.
    """
    formatted_output = ""
    for category, sub_categories in zillow_data.items():
        formatted_output += f"### {category.title()}\n"
        for sub_category_name, facts in sub_categories.items():
            fact_string = "; ".join(facts)
            formatted_output += f"* **{sub_category_name.title()}:** {fact_string}\n"
        formatted_output += "\n---\n"
    return formatted_output

# # Example Usage:
# zillow_data = {
#     'Interior': {'Bedrooms & bathrooms': ['Bedrooms: 1', 'Bathrooms: 2', '3/4 bathrooms: 2'], 'Heating': ['Natural Gas, Stove'], 'Cooling': ['None'], 'Appliances': ['Included: Oven, Range, Refrigerator'], 'Features': ['Beamed Ceilings, Interior Steps', 'Flooring: Stone, Tile, Wood', 'Basement: Crawl Space', 'Has fireplace: No'], 'Interior area': ['Total structure area: 1,200', 'Total interior livable area: 1,200 sqft']},
#     'Property': {'Parking': ['Total spaces: 3', 'Parking features: None'], 'Accessibility': ['Accessibility features: Not ADA Compliant'], 'Features': ['Levels: Two,Multi/Split', 'Stories: 2'], 'Lot': ['Size: 0.29 Acres'], 'Details': ['Additional structures: Storage', 'Parcel number: 654420', 'Zoning: R-1, 2, 3, 4, 5, 6', 'Zoning description: residential', 'Special conditions: Standard']},
#     'Construction': {'Type & style': ['Home type: SingleFamily', 'Architectural style: Multi-Level,Northern New Mexico', 'Property subtype: Single Family Residence'], 'Materials': ['Adobe, Frame', 'Foundation: Basement', 'Roof: Metal,Pitched'], 'Condition': ['Year built: 1870']},
#     'Utilities & green energy': {'Miscellaneous': ['Sewer: Public Sewer', 'Water: Public', 'Utilities for property: Electricity Available']},
#     'Community & hoa': {'HOA': ['Has HOA: No'], 'Location': ['Region: Las Vegas']},
#     'Financial & listing details': {'Miscellaneous': ['Price per square foot: $208/sqft', 'Tax assessed value: $135,283', 'Annual tax amount: $1,303', 'Date on market: 7/29/2025', 'Cumulative days on market: 29 days', 'Listing terms: Cash,New Loan']}
# }

# formatted_description = format_zillow_data(zillow_data)
# print(formatted_description)


def format_zillow_stats(zillow_stats):
    """
    Formats Zillow stats

    Args:
        zillow_stats (dict): The dictionary containing property stats.

    Returns:
        str: A Markdown-formatted string of the property stats.
    """
    formatted_output = "### Zillow Stats\n"
    for key, value in zillow_stats.items():
        formatted_output += f"* **{key.replace('_', ' ').capitalize()}:** {value}\n"
    formatted_output += "\n---\n\n"
    return formatted_output 

def extract_source_info(mls_info_div):
    """
    Extracts source, MLS number, and originating MLS from the given div.
    This function uses a more robust approach by looking for key strings,
    as the class names are prone to change.
    """
    source_data = {}
    # Find the div that contains the source information.
    # We use a lambda function to find any class that contains 'Spacer',
    # as this is more likely to be stable than the full class name.
    # The search is restricted to the mls_info_div passed to this function.
    source_info_div = mls_info_div.find('div', class_=lambda x: x and 'Spacer' in x)
    if source_info_div:
        # Get all span tags within the identified div
        spans = source_info_div.find_all('span')
        for span in spans:
            text = span.get_text(strip=True)
            if "Source:" in text:
                # Remove prefix, then the trailing comma, and finally strip whitespace
                clean_text = text.replace('Source:', '').replace(',', '').strip()
                source_data['Source'] = clean_text
            elif "MLS#:" in text:
                # Remove prefix, then the trailing comma, and finally strip whitespace
                clean_text = text.replace('MLS#:', '').replace(',', '').strip()
                source_data['MLS#'] = clean_text
            elif "Originating MLS:" in text:
                # Remove prefix, then the trailing comma, and finally strip whitespace
                clean_text = text.replace('Originating MLS:', '').replace(',', '').strip()
                source_data['Originating MLS'] = clean_text
    return source_data

def extract_mls_data(html_content):
    """
    Extracts MLS information from a given HTML string.

    Args:
        html_content (str): The HTML content of the webpage.

    Returns:
        dict: A dictionary containing the extracted MLS data.
    """
    soup = BeautifulSoup(html_content, 'lxml')

    data = {}

    # Find the main MLS information div
    mls_info_div = soup.find('div', {'aria-label': 'MLS information'})
    if not mls_info_div:
        print("Could not find the main MLS information div.")
        return data

    # Extract the 'Listing updated' date
    listing_updated_tag = mls_info_div.find('p', {'data-testid': 'current-list-attribution-last-updated'})
    if listing_updated_tag:
        # The text is split across a <span> and a text node, so we use .get_text()
        data['Listing updated'] = listing_updated_tag.get_text(strip=True).replace('Listing updated:', '').strip()

    # Extract the agent and broker information
    listed_by_div = mls_info_div.find('div', {'data-testid': 'seller-attribution'})
    if listed_by_div:
        agent_tag = listed_by_div.find('p', {'data-testid': 'attribution-LISTING_AGENT'})
        if agent_tag:
            # .get_text(separator=' ', strip=True) joins the text nodes with a space
            data['Listed by agent'] = agent_tag.get_text(separator=' ', strip=True)

        broker_tag = listed_by_div.find('p', {'data-testid': 'attribution-BROKER'})
        if broker_tag:
            data['Listed by broker'] = broker_tag.get_text(separator=' ', strip=True)

    # Extract source, MLS number, and originating MLS using the new helper function
    source_info = extract_source_info(mls_info_div)
    data.update(source_info)

    return data




def format_scrape(scrapes_folder_path = default_scrapes_path, output_folder_path = default_scrapes_path):
    
    scrapes_folder = Path(scrapes_folder_path)
    output_folder = Path(output_folder_path)
    # Create the output directory if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)
    print(f"Parsed files will be saved in: {output_folder}")

    print('Scrape Zillow listings')

    # Check if the directory exists first
    try:
        if not scrapes_folder.is_dir():
            raise FileNotFoundError(f"The directory '{scrapes_folder}' was not found.")

    except FileNotFoundError:
        print(f"Error: The folder {zlw_files} was not found.")
        sys.exit(1)

    # Use a generator expression to find all files with a .zlw extension
    zlw_files = scrapes_folder.glob('*.zlw')
        
    print(f"\nListings from: {scrapes_folder}")

    for file_path in zlw_files:

        file_lines = [] 
        
        # Print the name of the file being processed
        print(f"Reading content from: {file_path.name}")
    
        try:
            # Open the file for reading ('r') with the 'with' statement
            with open(file_path, 'r', encoding='utf-8') as f:
                # Read the entire content of the file into a single string
                content = f.read()
            stats = parse_zillow_stats(content)
            facts = parse_zillow_facts(content)
            listing_data = extract_mls_data(content)
            name = property_address_from_filename(file_path.name)
            image = extract_image_src(content)

            if image:
                print(f"![{name}]({image})")
                file_lines.append(f"![{name}]({image})")
            else:
                print("No image URL found.")

            address = get_formatted_address(name)
            print(f"\n## Property: {name}")
            file_lines.append(f"\n## Property: {name}")
            if address:
                print(f"## Address: {address}")
                file_lines.append(f"### Address: {address}")
            else:
                print("No formatted address found.")
                file_lines.append("No formatted address found.")

            # Get the MLS ID from the listing_data
            id = listing_data.get('MLS#', 'N/A')
            print(f"### MLS Property ID: {id}")
            file_lines.append(f"## MLS Property ID: {id}")

            print("\n---\n -- Stats --")

            if stats:
                #print(f"Stats for {url}:")
                for key, value in stats.items():
                    print(f"  - {key.replace('_', ' ').capitalize()}: {value}")
                    file_lines.append(f"  - {key.replace('_', ' ').capitalize()}: {value}")
            else:
                print(f"No stats retrieved for {name}.")
                file_lines.append(f"No stats retrieved for {name}.")

            print("\n---\n")
            if listing_data:
                print("## MLS Data:")
                file_lines.append("## MLS Data:")
                for key, value in listing_data.items():
                    print(f"  - {key}: {value}")
                    file_lines.append(f"  - {key}: {value}")
            else:
                print(f"No MLS data retrieved for {name}.")  
                file_lines.append(f"No MLS data retrieved for {name}.")

            print("\n---\n")

            if facts:
                formatted_description = format_zillow_data(facts)
                print("## Facts:")
                file_lines.append("## Facts:")
                file_lines.append(formatted_description)
                print(formatted_description)
            else:
                print(f"No facts retrieved for {name}.")
                file_lines.append(f"No facts retrieved for {name}.")

            print("\n---\n")
            file_lines.append("\n---\n")
                    
            save_file_lines(file_lines, Path(output_folder) / (file_path.name + '.md'))

            print(f"Finished processing {file_path.name}")

        except IOError as e:
            # Catch any potential file I/O errors (e.g., permission denied)
            print(f"Error reading file {file_path}: {e}")
        except UnicodeDecodeError as e:
            # Catch encoding errors if the file isn't UTF-8
            print(f"Encoding error with file {file_path}: {e}")

    

def main():

    """Main function to handle command-line arguments and run the scraper."""
    parser = argparse.ArgumentParser(description='Scrape Zillow listing from scrape folder.')
   # Add the 'scrapes_folder' argument with the absolute default path
    parser.add_argument('scrapes_folder', 
                    nargs='?', 
                    default=default_scrapes_path,
                    help=f'Path to a folder containing Zillow html scrapes. Defaults to "{default_scrapes_path}" if not provided.')
    parser.add_argument('-o', '--output_folder', 
                        type=str, 
                        default=default_scrapes_path,
                        help=f'Path to the output folder for scraped files. Defaults to "{default_scrapes_path}" if not provided.')
    
    args = parser.parse_args()  
    format_scrape(args.scrapes_folder, args.output_folder)
        
if __name__ == "__main__":
    main()


