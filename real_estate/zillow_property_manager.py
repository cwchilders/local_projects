from urllib.parse import urlparse
import re


def get_property_id_from_url(url):
    """
    Extracts the unique Zillow Property ID (ZPID) from the URL.
    This version handles multiple URL formats, including the zpid in the path.
    """
    parsed_url = urlparse(url)
    
    # New: Match the /123456_zpid/ pattern in the path
    zpid_path_match = re.search(r'(\d+)_zpid', parsed_url.path)
    if zpid_path_match:
        return zpid_path_match.group(1)

    # Old: A Zillow URL typically has the ZPID as the last segment before the trailing slash
    # e.g., /b/309-floresta-st-las-vegas-nm-123456/
    path_segments = parsed_url.path.split('/')
    for segment in reversed(path_segments):
        if segment.isdigit():
            return segment
            
    # Old: For older URLs, the ID is part of the query
    zpid_query_match = re.search(r'zpid=(\d+)', parsed_url.query)
    if zpid_query_match:
        return zpid_query_match.group(1)
    # nope --nada...
    return None


def get_property_name(url):
    """
    Extracts a human-readable property name from a Zillow URL.
    """
    try:
        # Regex to capture the address part of the URL
        # It looks for "homedetails/" followed by a non-greedy match of any characters
        # up to the next slash. The non-greedy `(.*?)` is key here.
        match = re.search(r'homedetails/(.*?)/.*_zpid', url)
        if match:
            # The address is in the first capture group
            address_segment = match.group(1)
            # Replace hyphens with spaces for a cleaner look
            return address_segment.replace('-', ' ')
        else:
            # Fallback for URLs that don't follow the 'homedetails' pattern
            # This handles cases like `.../address/zpid_...`
            match = re.search(r'.com/(.*?)/.*_zpid', url)
            if match:
                address_segment = match.group(1)
                return address_segment.replace('-', ' ')
            
            return "Unknown Property"

    except Exception as e:
        print(f"Error extracting property name from URL: {e}")
        return "Unknown Property"
    
    return "Unknown Property"


# This block ensures the code below only runs if the script is executed directly
# and not when it's imported as a module.
if __name__ == "__main__":
    # Example usage for testing the parsing functions
    print("This is a test run of the parse_zillow_page.py module.")
    print("This output should not appear when the file is imported.")
    # You can add test calls to your parsing functions here
    # Example:
    # with open('example_zillow_page.html', 'r') as f:
    #     html_content = f.read()
    # stats = parse_zillow_stats(html_content)
    # print(stats)