import requests
import json
from typing import Dict


# ----------------------------
# Function Definitions
# ----------------------------
def autocomplete_address(
        lightbox_api_key: str, 
        address: str, 
        country_code: str
) -> Dict:
    """
    Autocompletes the provided address using the LightBox API.
    
    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
        address (str): The partial address to be autocompleted.
        country_code (str): The ISO 3166-1 alpha-2 country code.
    
    Returns:
        dict: The autocompleted address information in JSON format.
    """
    # Prepare request parameters
    BASE_URL = "https://api.lightboxre.com/v1"
    ENDPOINT = "/addresses/_autocomplete"
    URL = BASE_URL + ENDPOINT
    params = {'text': address, 'countryCode': country_code}
    headers = {'x-api-key': lightbox_api_key}

    # Send request to LightBox API
    response = requests.get(URL, params=params, headers=headers)

    return response


def test_autocomplete_address_response_status(lightbox_api_key: str) -> None:
    # Test case for successful request (HTTP status code 200)
    address = '5201 California A'
    country_code = 'US'
    address_search_data = autocomplete_address(lightbox_api_key, address, country_code)
    assert address_search_data.status_code == 200, f"Expected status code 200, but got {address_search_data.status_code}"

    # Test case for unsuccessful request (HTTP status code 400)
    address = '5201 California A'
    country_code = 'U' # Invalid country_code
    address_search_data = autocomplete_address(lightbox_api_key, address, country_code)
    assert address_search_data.status_code == 400, f"Expected status code 400, but got {address_search_data.status_code}"

    # Test case for unsuccessful request (HTTP status code 400)
    address = '?' # Invalid address
    country_code = 'US'
    address_search_data = autocomplete_address(lightbox_api_key, address, country_code)
    assert address_search_data.status_code == 400, f"Expected status code 400, but got {address_search_data.status_code}"

    # Test case for unsuccessful request (HTTP status code 401)
    address = '5201 California A'
    country_code = 'US'
    address_search_data = autocomplete_address(lightbox_api_key+"A", address, country_code) # Invalid API Key
    assert address_search_data.status_code == 401, f"Expected status code 401, but got {address_search_data.status_code}"



# ----------------------------
# API Usage
# ----------------------------
lightbox_api_key = '<YOUR_API_KEY>'
address = '5201 California A'
country_code = 'US'

address_search_data = autocomplete_address(lightbox_api_key, address, country_code)
print(f"status_code: {address_search_data.status_code}")
print(json.dumps(address_search_data.json(), indent=4))


# ----------------------------
# API Testing
# ----------------------------
test_status = test_autocomplete_address_response_status(lightbox_api_key)