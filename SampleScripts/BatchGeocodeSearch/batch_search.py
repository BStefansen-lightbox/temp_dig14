import requests
import pandas as pd
from typing import Dict, List


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

# Function to read addresses from a CSV file and format them.
def read_addresses_from_csv(file_path: str) -> List[str]:
    """
    Reads addresses from a CSV file and formats them into 'Address, City State Zip Code'.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        List[str]: A list of formatted address strings.
    """
    df = pd.read_csv(file_path)

    # Concatenating address components into a single address string per row
    formatted_addresses = df.apply(
        lambda row: f"{row['Address']}, {row['City']} {row['State']} {row['Zip Code']}", 
        axis=1
    )
    return formatted_addresses.tolist()

# Function to batch process addresses for geocoding.
def batch_geocode_addresses(api_key: str, addresses: List[str], batch_size: int = 200) -> pd.DataFrame:
    """
    Batch processes a list of addresses for geocoding.

    Args:
        api_key (str): API key for the geocoding service.
        addresses (List[str]): List of addresses to geocode.
        batch_size (int): Number of addresses to process in each batch.
    
    Returns:
        pd.DataFrame: DataFrame containing original addresses and expanded geocoded data.
    """
    batched_addresses = [addresses[i:i + batch_size] for i in range(0, len(addresses), batch_size)]
    all_results = []

    for batch in batched_addresses:
        for address in batch:
            result = geocode_address(api_key, address)
            if result.status_code == 200:
                data = result.json()
                # Extracting data from the first match
                if data['addresses']:
                    first_match = data['addresses'][0]
                    latitude = first_match['location']['representativePoint']['latitude']
                    longitude = first_match['location']['representativePoint']['longitude']
                    confidence_score = first_match['$metadata']['geocode']['confidence']['score']
                    precision_code = first_match['$metadata']['geocode']['precisionCode']  # Extracting precision code
                    all_results.append({
                        "address": address, 
                        "latitude": latitude, 
                        "longitude": longitude, 
                        "confidence_score": confidence_score,
                        "precision_code": precision_code  # Adding precision code to the DataFrame
                    })
                else:
                    all_results.append({
                        "address": address, 
                        "latitude": "No match", 
                        "longitude": "No match", 
                        "confidence_score": "No match",
                        "precision_code": "No match"
                    })
            else:
                all_results.append({
                    "address": address, 
                    "latitude": "Failed",
                    "longitude": f"Status Code: {result.status_code}",
                    "confidence_score": "Failed",
                    "precision_code": "Failed"
                })
                print(f"Failed to geocode address '{address}', Status Code: {result.status_code}")

    return pd.DataFrame(all_results)


# Testing function for verifying the response status of the geocode_address function
def test_geocode_address_response_status(lightbox_api_key: str) -> None:
    # Test cases for different scenarios
    # Each test case asserts the expected HTTP status code

    # Test case for successful request (HTTP status code 200)
    address = '25482 Buckwood Land Forest, Ca, 92630'
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 200, f"Expected status code 200, but got {address_search_data.status_code}"

    # Test case for request with empty address (HTTP status code 400)
    address = ''
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 400, f"Expected status code 400, but got {address_search_data.status_code}"

    # Test case with invalid API key (HTTP status code 401)
    address = '25482 Buckwood Land Forest, Ca, 92630'
    address_search_data = geocode_address("Invalid-LightBox-Key", address)
    assert address_search_data.status_code == 401, f"Expected status code 401, but got {address_search_data.status_code}"

    # Test case with incomplete address (HTTP status code 404)
    address = '25482 Buckwood Land Forest'
    address_search_data = geocode_address(lightbox_api_key, address)
    assert address_search_data.status_code == 404, f"Expected status code 404, but got {address_search_data.status_code}"

# ----------------------------
# API Usage
# ----------------------------

lightbox_api_key = 'your_api_key'  # Replace with the actual API key
input_file_path = input('Enter your input file name: ')  # User inputs the file name
output_file_path = input('Enter your output file name: ')  # User inputs the output file name

# Reading and processing addresses
print("Reading addresses from CSV file...")
addresses = read_addresses_from_csv(input_file_path)
print("Starting batch geocoding...")
geocoded_data = batch_geocode_addresses(lightbox_api_key, addresses)
print("Batch geocoding completed.")

# Saving geocoded data to output file
geocoded_data.to_csv(output_file_path, index=False)
print(f"Geocoded data saved to '{output_file_path}'.")

# ----------------------------
# API Testing
# ----------------------------

print("Starting API tests...")
test_geocode_address_response_status(lightbox_api_key)
print("API tests completed.")
