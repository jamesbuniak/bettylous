import csv

def extract_addresses(input_file, output_file):
    """Extract and format addresses from CSV file."""
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for row in reader:
                address = row['Address'].strip()
                city = row['City'].strip().title()
                state = row['State'].strip().upper()
                zip_code = row['Zip'].strip()

                formatted = f"{address}, {city} {state}, {zip_code}"
                outfile.write(formatted + '\n')

    print(f"Extracted addresses to {output_file}")

if __name__ == '__main__':
    extract_addresses('addresses.csv', 'addresses_formatted.txt')
