import requests
import xml.etree.ElementTree as ET
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

# URL for fetching the XML data
base_url = "http://challenge.ctf.games:32154/bucket"

def fetch_keys():
    # Step 1: Fetch the XML data from the server
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to fetch XML data. Status code: {response.status_code}")
        return []

    # Parse the XML with namespace handling
    keys = []
    root = ET.fromstring(response.text)

    # Define the namespace and find all Key elements
    namespace = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
    for content in root.findall("s3:Contents", namespace):
        key = content.find("s3:Key", namespace).text
        if key:
            keys.append(key)
    return keys

def download_and_decode_key(key):
    # Construct the full URL for the key
    key_url = f"{base_url}/{key}"
    
    # Step 3: Download the content for each key
    response = requests.get(key_url)
    if response.status_code != 200:
        print(f"Failed to download content for key: {key}. Status code: {response.status_code}")
        return None
    
    # Step 4: Decode the content from Base64
    if "flag" in response.text:
        print(response.text)

def main():
    # Fetch the list of keys
    keys = fetch_keys()
    if not keys:
        print("No keys found.")
        return
    
    # Process each key using threading to speed up downloads
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_key = {executor.submit(download_and_decode_key, key): key for key in keys}
        
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                decoded_content = future.result()
                if decoded_content:
                    print(decoded_content)
            except Exception as exc:
                print(f"Error processing key {key}: {exc}")

if __name__ == "__main__":
    main()
