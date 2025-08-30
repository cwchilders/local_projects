import re
from bs4 import BeautifulSoup

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