import requests
import json
import os

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def get_city_from_address(address):
    """
    Uses the Google Maps Geocoding API to find the city from an address.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        
        # Check if the API returned a valid result
        if data['status'] == 'OK':
            # Extract the city from the address components
            address_components = data['results'][0]['address_components']
            for component in address_components:
                # 'locality' is the type for the city
                if 'locality' in component['types']:
                    return component['long_name']
                    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except (KeyError, IndexError):
        # Handle cases where the expected data structure is not found
        print("Could not parse city from API response.")
    
    return None


def get_formatted_address(address):
    """
    Uses the Google Maps Geocoding API to get the formatted address.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        
        # Check if the API returned a valid result
        if data['status'] == 'OK':
            return data['results'][0]['formatted_address']
                    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except (KeyError, IndexError):
        # Handle cases where the expected data structure is not found
        print("Could not parse formatted address from API response.")
    
    return None

if __name__ == "__main__":
    # Example usage
    address = "194 State Road 573 Espanola NM 87575"
    city = get_city_from_address(address)
    address = get_formatted_address(address)
    print(f"Formatted Address: {address}")

    if city:
        print(f"The city is: {city}")
    else:
        print("City not found or API request failed.")