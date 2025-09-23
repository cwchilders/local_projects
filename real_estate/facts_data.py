from bs4 import BeautifulSoup
import re

def extract_facts_and_features(html_content):
    """
    Extracts facts and features from the provided HTML content.

    Args:
        html_content: A string containing the HTML.

    Returns:
        A dictionary containing the facts and features, organized by category,
        or None if the main container is not found.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    facts_module = soup.find('div', attrs={'data-testid': 'facts-and-features-module'})

    if not facts_module:
        return None

    facts_data = {}
    category_groups = facts_module.find_all('div', attrs={'data-testid': 'category-group'})

    for group in category_groups:
        group_heading_h3 = group.find('h3', class_=re.compile("StyledCategoryGroupHeading"))
        if not group_heading_h3:
            continue
        group_name = group_heading_h3.get_text(strip=True)
        facts_data[group_name] = {}

        fact_categories = group.find_all('div', attrs={'data-testid': 'fact-category'})
        for category in fact_categories:
            category_heading_h6 = category.find('h6', class_=re.compile("StyledFactCategoryHeading"))
            # Use "General" if no h6 heading is found
            category_name = category_heading_h6.get_text(strip=True) if category_heading_h6 else "General"
            
            facts_list = category.find('ul', class_=re.compile("StyledFactCategoryFactsList"))
            if facts_list:
                facts = [li.get_text(strip=True) for li in facts_list.find_all('li')]
                if category_name in facts_data[group_name]:
                    facts_data[group_name][category_name].extend(facts)
                else:
                    facts_data[group_name][category_name] = facts

    return facts_data
