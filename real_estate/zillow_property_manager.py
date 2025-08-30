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
    Extracts the property name from a Zillow URL.
    
    The name is typically the segment between 'homedetails/' and the ZPID.
    
    Args:
        url (str): The full Zillow URL.
        
    Returns:
        str: The extracted property name, with hyphens replaced by spaces.
    """
    try:
        # Find the starting point in the URL
        start_index = url.find('homedetails/') + len('homedetails/')
        if start_index < len('homedetails/'):
            return "Unknown Property"
        
        # Find the end point by looking for the '_zpid' part
        # This is more reliable as it doesn't rely on the final slash
        end_index = url.find('_zpid/')
        if end_index == -1:
            end_index = url.rfind('/')

        # Extract the segment and replace hyphens with spaces
        property_segment = url[start_index:end_index]
        return property_segment.replace('-', ' ')
        
    except Exception as e:
        print(f"Error extracting property name from URL: {e}")
        return "Unknown Property"
    
# Example usage:
# url = "https://www.zillow.com/homedetails/309-Floresta-St-Las-Vegas-NM-87701/123456_zpid/"
# print(get_property_id_from_url(url))  # Output: 123456
# print(get_property_name(url)) # Output: "309 Floresta St Las Vegas NM 87701"     