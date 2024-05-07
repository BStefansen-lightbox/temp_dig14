import requests
import json
from typing import Dict

# ----------------------------
# Function Definitions
# ----------------------------

# Function to take a LightBox ID and Country Code, and a Common Ownership flag to determine adjacent parcels with a common owner
def get_common_owners(lightbox_api_key: str, country_code: str, id: str, common_ownership: str) -> Dict:
    """
    Query for adjacent parcel(s) with a common owner using the LightBox parcel 'ID.'
    
    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
        id (str): The LightBox ID for the specified parcel.
        country_code (str): ISO 3166 alpha-2 country code (e.g., 'us' for the United States). 
        common_ownership (boolean): Flag to return only parcels that have a common ownership with the target parcel ID. If false return parcels that intersect the parcel noted by the parcel LightBox ID.
    Returns:
        dict: The parcel information in JSON format.
    """
    # API endpoint configuration
    BASE_URL = "https://api.lightboxre.com/v1"
    ENDPOINT = f"/parcels/_adjacent/{country_code}/{id}?commonOwnership='{common_ownership}'" # Concatenate endpoint with country code, id and common ownership value
    URL = BASE_URL + ENDPOINT

    # Setting up request parameters and headers
    headers = {'x-api-key': lightbox_api_key}

    # Sending request to the LightBox API
    response = requests.get(URL, headers=headers)
    return response

# Function to test the response status of the get_common_owners function.
def test_response_status(lightbox_api_key: str) -> None:
    """
    Tests the response status for various scenarios using the get_common_owners function.

    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
    """
    common_ownership = 'true'

    # Test for a successful request (HTTP status code 200)
    id = '0201MABNPDBU5D2EGP08YA'
    country_code = 'us'
    data = get_common_owners(lightbox_api_key, country_code, id, common_ownership)
    assert data.status_code == 200, f"Expected status code 200, but got {data.status_code}"

    # Test for an unsuccessful request due to a null LightBoxID (HTTP status code 400)
    id = ''  # No LightBoxID specified
    country_code = 'us' # Invalid Country Code
    data = get_common_owners(lightbox_api_key, country_code, id, common_ownership)
    assert data.status_code == 400, f"Expected status code 400, but got {data.status_code}"

    # Test for an unsuccessful request due to an invalid API key (HTTP status code 401)
    id = '0201MABNPDBU5D2EGP08YA'
    country_code = 'us'
    data = get_common_owners("My LightBox Key", country_code, id, common_ownership)  # Invalid API key
    assert data.status_code == 401, f"Expected status code 401, but got {data.status_code}"

    # Test for an unsuccessful request due to an invalid LightBoxID (HTTP status code 404)
    id = '0201MAA'  # Invalid LightBoxID
    country_code = 'us'
    data = get_common_owners(lightbox_api_key, country_code, id, common_ownership)
    assert data.status_code == 404, f"Expected status code 404, but got {data.status_code}"

# ----------------------------
# API Usage
# ----------------------------

# Assign your LightBox API key
lightbox_api_key = '<YOUR_API_KEY>'

# Specify the LightBoxID
id = '0201MABNPDBU5D2EGP08YA'

# Specify the Country Code
country_code = "us"

# Pass in common_ownership=true and get only the parcels adjacent to this parcel that have common ownership.
common_ownership = "true"

# Get the parcel data for the specified LightBoxID
data = get_common_owners(lightbox_api_key, country_code, id, common_ownership)

# Print the common ownership data in a readable JSON format
print(json.dumps(data.json(), indent=4))

# ----------------------------
# API Testing
# ----------------------------

# Perform tests to verify the response status of the get_common_owners function
test_status = test_response_status(lightbox_api_key)
