import requests
import json
from typing import Dict

# ----------------------------
# Function Definitions
# ----------------------------

# Function to take a LightBox ID as a parameter and return the associated Demographic data
def get_demographics(lightbox_api_key: str, id: str) -> Dict:
    """
    Query for demographic record identified by a LightBox Parcel 'ID.'
    
    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
        id (str): The LightBox ID for the specified parcel.
    
    Returns:
        dict: The parcel information in JSON format.
    """
    # API endpoint configuration
    BASE_URL = "https://api.lightboxre.com/v1"
    ENDPOINT = f"/demographics/_on/parcel/us/{id}" # Concatenate endpoint with the id
    URL = BASE_URL + ENDPOINT

    # Setting up request parameters and headers
    headers = {'x-api-key': lightbox_api_key}

    # Sending request to the LightBox API
    response = requests.get(URL, headers=headers)
    return response

# Function to test the response status of the get_demographics function.
def test_response_status(lightbox_api_key: str) -> None:
    """
    Tests the response status for various scenarios using the get_demographics function.

    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
    """

    # Test for a successful request (HTTP status code 200)
    id = '0201MABNPDBU5D2EGP08YA'
    data = get_demographics(lightbox_api_key, id)
    assert data.status_code == 200, f"Expected status code 200, but got {data.status_code}"

    # Test for an unsuccessful request due to a null LightBoxID (HTTP status code 400)
    id = ''  # No LightBoxID specified
    data = get_demographics(lightbox_api_key, id)
    assert data.status_code == 400, f"Expected status code 400, but got {data.status_code}"

    # Test for an unsuccessful request due to an invalid API key (HTTP status code 401)
    id = '0201MABNPDBU5D2EGP08YA'
    data = get_demographics("My LightBox Key", id)  # Invalid API key
    assert data.status_code == 401, f"Expected status code 401, but got {data.status_code}"

    # Test for an unsuccessful request due to an invalid LightBox ID (HTTP status code 404)
    id = '0201MAA'  # Invalid LightBoxID
    data = get_demographics(lightbox_api_key, id)
    assert data.status_code == 404, f"Expected status code 404, but got {data.status_code}"

# ----------------------------
# API Usage
# ----------------------------

# Assign your LightBox API key
lightbox_api_key = '<YOUR_API_KEY>'

# Specify the LightBoxID
id = '0201MABNPDBU5D2EGP08YA'

# Get the parcel data for the specified LightBoxID
data = get_demographics(lightbox_api_key, id)

# # Print the geocoded address data in a readable JSON format
print(json.dumps(data.json(), indent=4))

# ----------------------------
# API Testing
# ----------------------------

# Perform tests to verify the response status of the get_demographics function
test_status = test_response_status(lightbox_api_key)
