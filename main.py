import csv
import os
from playwright.sync_api import sync_playwright

def scrape_distributors(zip_code):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"https://www.uniprofoodservice.com/distributors/directory?radius=100&search={zip_code}"
        page.goto(url)
        page.wait_for_selector('.overflow-y-scroll.overscroll-none.scrollbar-public.divide-y')

        distributors = []
        elements = page.query_selector_all('.grid.grid-cols-4.group.hover\\:bg-gray-100')

        for el in elements:
            name = el.query_selector('span').inner_text()
            
            # Use XPath for complex class selectors
            location = el.query_selector("xpath=.//span[contains(@class, 'hidden') and contains(@class, '2xl:flex')]") or "N/A"
            location = location.inner_text() if location != "N/A" else location
            
            dist_type = el.query_selector("xpath=.//span[contains(@class, 'flex') and contains(@class, '2xl:hidden')][1]") or "N/A"
            dist_type = dist_type.inner_text() if dist_type != "N/A" else dist_type
            
            distance = el.query_selector("xpath=.//span[contains(@class, 'flex') and contains(@class, '2xl:hidden')][2]") or "N/A"
            distance = distance.inner_text() if distance != "N/A" else distance

            distributors.append({
                "name": name,
                "location": location,
                "distribution_type": dist_type,
                "distance": distance
            })

        browser.close()
        return distributors

def main():
    input_file = 'input.csv'
    output_file = 'output.csv'
    
    # Detect CSV headers (case-insensitive, handle BOM)
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        original_headers = next(reader)
        headers_lower = [h.strip().lower() for h in original_headers]
        
        # Create mapping from lowercase to original headers
        header_map = {h.lower(): h for h in original_headers}
        
        zip_header = next((h for h in headers_lower if h in ['zip', 'zipcode']), None)
        city_header = 'city' if 'city' in headers_lower else None
        state_header = 'state' if 'state' in headers_lower else None
        county_header = 'county' if 'county' in headers_lower else None

    if not zip_header:
        raise ValueError("No ZIP/Zipcode column found in input.csv")

    fieldnames = [
        header_map[zip_header],
        header_map.get('city', 'City'),
        header_map.get('state', 'State'),
        header_map.get('county', 'County'),
        'name', 'location', 'distribution_type', 'distance'
    ]

    # Ensure output file has header
    if not os.path.exists(output_file) or os.stat(output_file).st_size == 0:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    with open(input_file, 'r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        
        for row in reader:
            # Get ZIP value with case-insensitive matching
            zip_code = row.get(header_map[zip_header], row.get(zip_header.upper()))
            
            print(f"Processing ZIP: {zip_code}")
            
            try:
                distributors = scrape_distributors(zip_code)
                
                # Append results immediately after ZIP processing
                with open(output_file, 'a', newline='', encoding='utf-8') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    
                    for d in distributors:
                        merged_data = {
                            header_map[zip_header]: zip_code,
                            header_map['city']: row.get(header_map['city'], 'N/A'),
                            header_map['state']: row.get(header_map['state'], 'N/A'),
                            header_map['county']: row.get(header_map['county'], 'N/A'),
                            **d
                        }
                        writer.writerow(merged_data)
                    
            except Exception as e:
                print(f"Error processing {zip_code}: {str(e)}")
                continue

if __name__ == "__main__":
    main()