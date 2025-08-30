from bs4 import BeautifulSoup
import re

def parse_zillow_stats(html_content):
    """
    Parses Zillow stats from an HTML string using BeautifulSoup and regex.

    Args:
        html_content (str): The HTML snippet containing the stats.

    Returns:
        dict: A dictionary with the parsed stats, or None if the element is not found.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
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

# --- Example Usage ---
html_snippet = """
<dl class="styles__StyledOverviewStats-fshdp-8-111-1__sc-1x11gd9-0 kpgmGL">
	<dt><strong>204 days</strong></dt>
	<dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp">on Zillow</dt>
	<span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
	<dt><strong>1,188</strong></dt>
	<dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp"><button type="button" aria-expanded="false" aria-haspopup="false" class="TriggerText-c11n-8-111-1__sc-d96jze-0 hAKmPK TooltipPopper-c11n-8-111-1__sc-1v2hxhd-0 isapNu">views</button></dt>
	<span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
	<dt><strong>61</strong></dt>
	<dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp"><button type="button" aria-expanded="false" aria-haspopup="false" class="TriggerText-c11n-8-111-1__sc-d96jze-0 hAKmPK TooltipPopper-c11n-8-111-1__sc-1v2hxhd-0 isapNu">saves</button></dt>
	<span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
</dl>
"""

zillow_stats = parse_zillow_stats(html_snippet)

if zillow_stats:
    print(f"Days on Zillow: {zillow_stats['days_on_zillow']}")
    print(f"Views: {zillow_stats['views']}")
    print(f"Saves: {zillow_stats['saves']}")
else:
    print("Could not parse Zillow stats from the HTML.")

def parse_zillow_facts(html_content):
    """
    Parses Zillow facts from an HTML string using BeautifulSoup.

    Args:
        html_content (str): The HTML snippet containing the facts.

    Returns:
        dict: A nested dictionary with the parsed facts.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    data = {}
    for category_group in soup.find_all('div', {'data-testid': 'category-group'}):
        group_title = category_group.find('h3', class_=lambda x: x and 'StyledCategoryGroupHeading' in x).get_text(strip=True)
        data[group_title] = {}
        for fact_category in category_group.find_all('div', {'data-testid': 'fact-category'}):
            category_title_tag = fact_category.find('h6', class_=lambda x: x and 'StyledHeading' in x)
            category_title = category_title_tag.get_text(strip=True) if category_title_tag else 'Miscellaneous'
            data[group_title][category_title] = [li.get_text(strip=True) for li in fact_category.find_all('li')]

    print(data)
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
        formatted_output += "\n---\n\n"
    return formatted_output

# Example Usage:
zillow_data = {
    'Interior': {'Bedrooms & bathrooms': ['Bedrooms: 1', 'Bathrooms: 2', '3/4 bathrooms: 2'], 'Heating': ['Natural Gas, Stove'], 'Cooling': ['None'], 'Appliances': ['Included: Oven, Range, Refrigerator'], 'Features': ['Beamed Ceilings, Interior Steps', 'Flooring: Stone, Tile, Wood', 'Basement: Crawl Space', 'Has fireplace: No'], 'Interior area': ['Total structure area: 1,200', 'Total interior livable area: 1,200 sqft']},
    'Property': {'Parking': ['Total spaces: 3', 'Parking features: None'], 'Accessibility': ['Accessibility features: Not ADA Compliant'], 'Features': ['Levels: Two,Multi/Split', 'Stories: 2'], 'Lot': ['Size: 0.29 Acres'], 'Details': ['Additional structures: Storage', 'Parcel number: 654420', 'Zoning: R-1, 2, 3, 4, 5, 6', 'Zoning description: residential', 'Special conditions: Standard']},
    'Construction': {'Type & style': ['Home type: SingleFamily', 'Architectural style: Multi-Level,Northern New Mexico', 'Property subtype: Single Family Residence'], 'Materials': ['Adobe, Frame', 'Foundation: Basement', 'Roof: Metal,Pitched'], 'Condition': ['Year built: 1870']},
    'Utilities & green energy': {'Miscellaneous': ['Sewer: Public Sewer', 'Water: Public', 'Utilities for property: Electricity Available']},
    'Community & hoa': {'HOA': ['Has HOA: No'], 'Location': ['Region: Las Vegas']},
    'Financial & listing details': {'Miscellaneous': ['Price per square foot: $208/sqft', 'Tax assessed value: $135,283', 'Annual tax amount: $1,303', 'Date on market: 7/29/2025', 'Cumulative days on market: 29 days', 'Listing terms: Cash,New Loan']}
}

formatted_description = format_zillow_data(zillow_data)
print(formatted_description)


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