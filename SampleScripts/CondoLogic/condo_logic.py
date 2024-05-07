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
    params = {"text": address}
    headers = {"x-api-key": lightbox_api_key}

    # Sending request to the LightBox API
    geocoder_data = requests.get(URL, params=params, headers=headers)
    
    # Returning the geocoded address information
    return geocoder_data


# Test for the get_parcel_from_lbx_address_id() function
def get_parcel_data_from_address_coordinates(lightbox_api_key: str, country_code: str, address_coordinates: str) -> Dict:
    """
    Returns a dictionary containing the parcel data for the specified address.
    """

    # API endpoint configuration
    BASE_URL = "https://api.lightboxre.com/v1"
    ENDPOINT = f"/parcels/{country_code}/geometry"
    URL = BASE_URL + ENDPOINT

    # Setting up request parameters and headers
    params = {"wkt": address_coordinates}
    headers = {"x-api-key": lightbox_api_key}

    # Make the request
    parcel_data = requests.get(URL, params=params, headers=headers)
    
    # Return the parcel data
    return parcel_data


def get_assessment_data_from_lbx_parcel_id(lightbox_api_key: str, lbx_parcel_id: str) -> Dict:
    """
    Returns a dictionary containing the assessment data for the specified parcel.
    """

    # API endpoint configuration
    BASE_URL = "https://api.lightboxre.com/v1"
    ENDPOINT = f"/assessments/_on/parcel/us/{lbx_parcel_id}"
    URL = BASE_URL + ENDPOINT

    # Setting up request parameters and headers
    headers = {"x-api-key": lightbox_api_key}

    # Make the request
    assessment_data = requests.get(URL, headers=headers)
    
    # Return the assessment data
    return assessment_data


# Function to test the response status of the geocode_address function.
def test_geocode_address_response_status(lightbox_api_key: str) -> None:
    """
    Tests the response status for various scenarios using the geocode_address function.

    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
    """

    # Test for a successful request (HTTP status code 200)
    address = "25482 Buckwood Land Forest, Ca, 92630"
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 200, f"Expected status code 200, but got {address_search_data.status_code}"

    # Test for an unsuccessful request due to an empty address (HTTP status code 400)
    address = ""  # No address specified
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 400, f"Expected status code 400, but got {address_search_data.status_code}"

    # Test for an unsuccessful request due to an invalid API key (HTTP status code 401)
    address = "25482 Buckwood Land Forest, Ca, 92630"
    address_search_data = geocode_address("My-LightBox-Key", address)  # Invalid API key
    assert address_search_data.status_code == 401, f"Expected status code 401, but got {address_search_data.status_code}"

    # Test for an unsuccessful request due to an incomplete address (HTTP status code 404)
    address = "25482 Buckwood Land Forest"  # Incomplete address
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 404, f"Expected status code 404, but got {address_search_data.status_code}"


# Test the get_parcel_data_from_address_coordinates function
def test_get_parcel_data_from_address_coordinates(lightbox_api_key):
    """
    Test the get_parcel_data_from_address_coordinates function
    
    Args:
        lightbox_api_key (str): The LightBox API key
    """

    # Test for a successful request (HTTP status code 200)
    address = "25482 Buckwood Land Forest, Ca, 92630"
    country_code = "us"
    address_search_data = geocode_address(lightbox_api_key, address)
    address_coordinates = address_search_data.json()["addresses"][0]["location"]["representativePoint"]["geometry"]["wkt"]
    parcel_data = get_parcel_data_from_address_coordinates(lightbox_api_key, country_code, address_coordinates)
    assert parcel_data.status_code == 200, f"Expected status code 200, but got {parcel_data.status_code}"

    # Test for an unsuccessful request due to an invalid address ID (HTTP status code 400)
    address_coordinates = "foobar"
    parcel_data = get_parcel_data_from_address_coordinates(lightbox_api_key, country_code, address_coordinates)
    assert parcel_data.status_code == 400, f"Expected status code 400, but got {parcel_data.status_code}"

    # Test for an unsuccessful request due to an invalid API key (HTTP status code 401)
    parcel_data = get_parcel_data_from_address_coordinates(lightbox_api_key+"foobar", country_code, address_coordinates)
    assert parcel_data.status_code == 401, f"Expected status code 401, but got {parcel_data.status_code}"


# Test the get_parcel_data_from_lbx_parcel_id function
def test_get_assessment_data_from_lbx_parcel_id(lightbox_api_key):
    """
    Test the get_assessment_data_from_lbx_parcel_id function
    
    Args:
        lightbox_api_key (str): The LightBox API key
    """

    # Test for a successful request (HTTP status code 200)
    address = "25482 Buckwood Land Forest, Ca, 92630"
    country_code = "us"
    address_search_data = geocode_address(lightbox_api_key, address)
    address_coordinates = address_search_data.json()["addresses"][0]["location"]["representativePoint"]["geometry"]["wkt"]
    parcel_data = get_parcel_data_from_address_coordinates(lightbox_api_key, country_code, address_coordinates)
    parcel_id = parcel_data.json()["parcels"][0]["id"]
    assessment_data = get_assessment_data_from_lbx_parcel_id(lightbox_api_key, parcel_id)
    assert assessment_data.status_code == 200, f"Expected status code 200, but got {assessment_data.status_code}"

    # Test for an unsuccessful request due to an invalid parcel ID (HTTP status code 400)
    parcel_id = "1234567890"
    assessment_data = get_assessment_data_from_lbx_parcel_id(lightbox_api_key, parcel_id)
    assert assessment_data.status_code == 400, f"Expected status code 400, but got {assessment_data.status_code}"

    # Test for an unsuccessful request (HTTP status code 401)
    assessment_data = get_assessment_data_from_lbx_parcel_id(lightbox_api_key+"foobar", parcel_id)
    assert assessment_data.status_code == 401, f"Expected status code 401, but got {assessment_data.status_code}"


# ----------------------------
# API Usage
# ----------------------------

# Assign your LightBox API key
lightbox_api_key = ""

# Specify the address to geocode
address = "25482 Buckwood Land Forest, Ca, 92630"
country_code = "us" # 'us' for the United States

# Geocode the specified address
address_search_data = geocode_address(lightbox_api_key, address)

# Get the parcel data from the geocoded address
parcel_data = get_parcel_data_from_address_coordinates(lightbox_api_key, country_code, address_search_data.json()["addresses"][0]["location"]["representativePoint"]["geometry"]["wkt"])

# Get the assessment data from the parcel ID
assessment_data = get_assessment_data_from_lbx_parcel_id(lightbox_api_key, parcel_data.json()["parcels"][0]["id"])


# --------------------
# Print collected data
# --------------------

# Print the geocoded address data in a readable JSON format
print(json.dumps(address_search_data.json(), indent=4))
# Print the parcel data in a readable JSON format
print(json.dumps(parcel_data.json(), indent=4))
# Print the assessment data in a readable JSON format
print(json.dumps(assessment_data.json(), indent=4))


# ----------------------------
# API Testing
# ----------------------------

# Perform tests to verify the response status of the geocode_address function
test_geocode_address_response_status(lightbox_api_key)
test_get_parcel_data_from_address_coordinates(lightbox_api_key)
test_get_assessment_data_from_lbx_parcel_id(lightbox_api_key)
