from urllib.parse import urlparse
import re

def get_property_id_from_url(url):
    """
    Extracts the unique Zillow Property ID (ZPID) from the URL.
    """
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    
    # A Zillow URL typically has the ZPID as the last segment before the trailing slash
    # e.g., /b/309-floresta-st-las-vegas-nm-123456/
    # We look for a segment that is not empty and is likely the ZPID.
    for segment in reversed(path_segments):
        if segment.isdigit():
            return segment
            
    # For newer URLs like /homes/ZPID/, the ID is part of the path
    zpid_match = re.search(r'zpid_(\d+)', parsed_url.query)
    if zpid_match:
        return zpid_match.group(1)
        
    return None


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