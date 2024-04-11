import requests
import json
from typing import Dict


# ----------------------------
# Function Definitions
# ----------------------------
def reverse_address_search(
        lightbox_api_key: str, 
        wkt: str, 
        bufferDistance: float,
        bufferUnit: str,
        limit: int
) -> Dict:
    """
    Performs a reverse address search using the LightBox API.

    Args:
        lightbox_api_key (str): The API key for accessing the LightBox API.
        wkt (str): The geometry of the location expressed in WKT (well-known text) format.
                   Example: POINT(-117.852723 33.63799)
        bufferDistance (float): Buffer distance expressed in 'bufferUnits'.
                                Default value: 0
                                Example: 100
        bufferUnit (str): The unit type to apply to the buffer (e.g., m=meters, km=kilometers, ft=feet, or mi=miles).
                          Available values: m, km, ft, mi
                          Default value: m
                          Example: m
        limit (int): The maximum number of entries to return. If the value exceeds the maximum, then the maximum value will be used.

    Returns:
        dict: A dictionary containing information about the addresses found, in JSON format.
    """
    # Prepare request parameters
    BASE_URL = "https://api.lightboxre.com/v1"
    ENDPOINT = "/addresses/reverse"
    URL = BASE_URL + ENDPOINT
    params = {
        'wkt': wkt, 
        'bufferDistance': bufferDistance,
        'bufferUnit': bufferUnit,
        'limit': limit
    }
    headers = {'x-api-key': lightbox_api_key}

    # Send request to LightBox API
    response = requests.get(URL, params=params, headers=headers)

    return response


def test_reverse_address_search_status(lightbox_api_key: str) -> None:
    # Test case for successful request (HTTP status code 200)
    wkt = 'POINT(-117.852723 33.63799)'
    bufferDistance = 100
    bufferUnit = 'm'
    limit = 5

    address_search_data = reverse_address_search(
        lightbox_api_key, 
        wkt, 
        bufferDistance,
        bufferUnit,
        limit
    )
    assert address_search_data.status_code == 200, f"Expected status code 200, but got {address_search_data.status_code}"

    # Test case for unsuccessful request (HTTP status code 400)
    wkt = 'POINT(0)' # Invalid parameter
    bufferDistance = 100
    bufferUnit = 'm'
    limit = 5

    address_search_data = reverse_address_search(
        lightbox_api_key, 
        wkt, 
        bufferDistance,
        bufferUnit,
        limit
    )
    assert address_search_data.status_code == 400, f"Expected status code 400, but got {address_search_data.status_code}"

    # Test case for unsuccessful request (HTTP status code 400)
    wkt = 'POINT(-117.852723 33.63799)'
    bufferDistance = -1 # Invalid parameter
    bufferUnit = 'm'
    limit = 5

    address_search_data = reverse_address_search(
        lightbox_api_key, 
        wkt, 
        bufferDistance,
        bufferUnit,
        limit
    )
    assert address_search_data.status_code == 400, f"Expected status code 400, but got {address_search_data.status_code}"

    # Test case for unsuccessful request (HTTP status code 401)
    wkt = 'POINT(-117.852723 33.63799)'
    bufferDistance = 100
    bufferUnit = 'm'
    limit = 5

    address_search_data = reverse_address_search(
        lightbox_api_key+"foobar", 
        wkt, 
        bufferDistance,
        bufferUnit,
        limit
    )
    assert address_search_data.status_code == 401, f"Expected status code 401, but got {address_search_data.status_code}"



# ----------------------------
# API Usage
# ----------------------------
lightbox_api_key = '<YOUR_API_KEY>'
wkt = 'POINT(-117.852723 33.63799)'
bufferDistance = 100
bufferUnit = 'm'
limit = 5

address_search_data = reverse_address_search(
    lightbox_api_key, 
    wkt, 
    bufferDistance,
    bufferUnit,
    limit
)
print(f"status_code: {address_search_data.status_code}")
print(json.dumps(address_search_data.json(), indent=4))


# ----------------------------
# API Testing
# ----------------------------
test_reverse_address_search_status(lightbox_api_key)
