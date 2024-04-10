import requests
import json
from typing import Dict

# ----------------------------
# Function Definitions
# ----------------------------

# Function to geocode a single address using the LightBox API.
def geocode_address(lightbox_api_key: str, address: str) -> Dict:
    """
    Geocodes the provided address using the LightBox API.
    
    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
        address (str): The address string for matching.
    
    Returns:
        dict: The geocoded address information in JSON format.
    """
    # API endpoint configuration
    BASE_URL = "https://api.lightboxre.com/v1"
    ENDPOINT = "/addresses/search"
    URL = BASE_URL + ENDPOINT

    # Setting up request parameters and headers
    params = {'text': address}
    headers = {'x-api-key': lightbox_api_key}

    # Sending request to the LightBox API
    response = requests.get(URL, params=params, headers=headers)
    return response

# Function to test the response status of the geocode_address function.
def test_geocode_address_response_status(lightbox_api_key: str) -> None:
    """
    Tests the response status for various scenarios using the geocode_address function.

    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
    """

    # Test for a successful request (HTTP status code 200)
    address = '25482 Buckwood Land Forest, Ca, 92630'
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 200, f"Expected status code 200, but got {address_search_data.status_code}"

    # Test for an unsuccessful request due to an empty address (HTTP status code 400)
    address = ''  # No address specified
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 400, f"Expected status code 400, but got {address_search_data.status_code}"

    # Test for an unsuccessful request due to an invalid API key (HTTP status code 401)
    address = '25482 Buckwood Land Forest, Ca, 92630'
    address_search_data = geocode_address("My-LightBox-Key", address)  # Invalid API key
    assert address_search_data.status_code == 401, f"Expected status code 401, but got {address_search_data.status_code}"

    # Test for an unsuccessful request due to an incomplete address (HTTP status code 404)
    address = '25482 Buckwood Land Forest'  # Incomplete address
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 404, f"Expected status code 404, but got {address_search_data.status_code}"

# ----------------------------
# API Usage
# ----------------------------

# Assign your LightBox API key
lightbox_api_key = 'your_lightbox_api_key'

# Specify the address to geocode
address = '25482 Buckwood Land Forest, Ca, 92630'

# Geocode the specified address
address_search_data = geocode_address(lightbox_api_key, address)

# Print the geocoded address data in a readable JSON format
print(json.dumps(address_search_data.json(), indent=4))

# ----------------------------
# API Testing
# ----------------------------

# Perform tests to verify the response status of the geocode_address function
test_status = test_geocode_address_response_status(lightbox_api_key)
