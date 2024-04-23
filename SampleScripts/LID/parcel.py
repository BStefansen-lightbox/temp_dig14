import requests
import json
from typing import Dict

# ----------------------------
# Function Definitions
# ----------------------------

# Function to take a LightBox ID and Country Code as parameters and return the associated Parcel data
def get_parcel(lightbox_api_key: str, countryCode: str, id: str) -> Dict:
    """
    Query for a specific parcel using the LightBox parcel 'ID.'
    
    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
        id (str): The LightBox ID for the specified parcel.
        countryCode (str): ISO 3166 alpha-2 country code (e.g., 'US' for the United States). 
    
    Returns:
        dict: The parcel information in JSON format.
    """
    # API endpoint configuration
    BASE_URL = "https://api.lightboxre.com/v1"
    ENDPOINT = f"/parcels/{countryCode}/{id}" # Concatenate endpoint with country code and id
    URL = BASE_URL + ENDPOINT

    # Setting up request parameters and headers
    headers = {'x-api-key': lightbox_api_key}

    # Sending request to the LightBox API
    response = requests.get(URL, headers=headers)
    return response

# Function to test the response status of the get_parcel function.
def test_response_status(lightbox_api_key: str) -> None:
    """
    Tests the response status for various scenarios using the get_parcel function.

    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
    """

    # Test for a successful request (HTTP status code 200)
    id = '0201MABNPDBU5D2EGP08YA'
    countryCode = 'US'
    data = get_parcel(lightbox_api_key, countryCode, id)
    assert data.status_code == 200, f"Expected status code 200, but got {data.status_code}"

    # Test for an unsuccessful request due to a null LightBoxID (HTTP status code 400)
    id = ''  # No LightBoxID specified
    countryCode = '123' # Invalid Country Code
    data = get_parcel(lightbox_api_key, countryCode, id)
    assert data.status_code == 400, f"Expected status code 400, but got {data.status_code}"

    # Test for an unsuccessful request due to an invalid API key (HTTP status code 401)
    id = '0201MABNPDBU5D2EGP08YA'
    countryCode = 'US'
    data = get_parcel("My LightBox Key", countryCode, id)  # Invalid API key
    assert data.status_code == 401, f"Expected status code 401, but got {data.status_code}"

    # Test for an unsuccessful request due to an invalid LightBoxID (HTTP status code 404)
    id = '0201MAA'  # Invalid LightBoxID
    countryCode = 'US'
    data = get_parcel(lightbox_api_key, countryCode, id)
    assert data.status_code == 404, f"Expected status code 404, but got {data.status_code}"

# ----------------------------
# API Usage
# ----------------------------

# Assign your LightBox API key
lightbox_api_key = '<YOUR_API_KEY>'

# Specify the LightBoxID
id = '0201MABNPDBU5D2EGP08YA'

# Specify the Country Code
countryCode = "US"

# Get the parcel data for the specified LightBoxID
data = get_parcel(lightbox_api_key, countryCode, id)

# # Print the geocoded address data in a readable JSON format
print(json.dumps(data.json(), indent=4))

# ----------------------------
# API Testing
# ----------------------------

# Perform tests to verify the response status of the get_parcel function
test_status = test_response_status(lightbox_api_key)
