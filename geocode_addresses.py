import csv
import requests
import time
import os

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')

def geocode_address(address, api_key):
    """Geocode a single address using Google Geocoding API."""
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Failed to geocode: {address} - Status: {data['status']}")
        return None, None

def geocode_addresses(input_file, output_file, api_key):
    """Geocode all addresses from input file and write to CSV."""
    with open(input_file, 'r', encoding='utf-8') as infile:
        addresses = [line.strip() for line in infile if line.strip()]

    print(f"Geocoding {len(addresses)} addresses...")

    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['address', 'latitude', 'longitude'])

        for i, address in enumerate(addresses):
            lat, lng = geocode_address(address, api_key)
            writer.writerow([address, lat or '', lng or ''])

            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(addresses)} addresses")

            # Rate limit: Google allows 50 requests/second
            time.sleep(0.02)

    print(f"Results written to {output_file}")

if __name__ == '__main__':
    if not GOOGLE_API_KEY:
        print("Please set GOOGLE_API_KEY environment variable")
        print("  Windows: set GOOGLE_API_KEY=your_key_here")
        print("  Linux/Mac: export GOOGLE_API_KEY=your_key_here")
        exit(1)

    geocode_addresses('addresses_formatted.txt', 'data.csv', GOOGLE_API_KEY)
