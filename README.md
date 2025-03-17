# UniPro Foodservice Distributor Scraper

## Overview
This Python script uses Playwright to scrape distributor information from the UniPro Foodservice website for given ZIP codes. It merges the results with input location data and saves them to a CSV file.

---

## Features
- Scrapes distributor name, location, type, and distance from target URL
- Processes multiple ZIP codes from input CSV
- Merges scraped data with original CSV location data
- Auto-saves results incrementally to prevent data loss
- Handles case-insensitive CSV headers and encoding issues

---

## Requirements
1. Python 3.8+
2. Playwright dependencies:
   ```bash
   pip install playwright
   playwright install
   ```

---

## Input Format
Create `input.csv` with columns (case-insensitive):
```csv
ZIP,City,State,County
40003,Bagdad,KY,Shelby
40004,Bardstown,KY,Nelson
```

---

## Usage
1. **Prepare input file**:
   ```bash
   cp input.csv.example input.csv  # Create from example template
   ```

2. **Run the script**:
   ```bash
   python main.py
   ```

3. **Check output**:
   Results saved to `output.csv` with columns:
   ```
   ZIP | City | State | County | name | location | distribution_type | distance
   ```

---

## Configuration
Modify these parameters in `main()` function if needed:
- `radius=100` in URL (scrape area radius)
- `headless=True` (set to `False` for browser visibility)
- Output filename (`output.csv`)

---

## Troubleshooting
1. **Missing headers**:
   - Ensure `input.csv` has ZIP/Zipcode column
   - Verify column names match (City/State/County)

2. **Network errors**:
   - Check internet connection
   - Add `time.sleep()` between requests if blocked

3. **Site structure changes**:
   - Update CSS/XPath selectors in `scrape_distributors()`

---

## Notes
- **Rate limiting**: Add delays between requests if targeting many ZIP codes
- **Compliance**: Ensure usage complies with UniPro's terms of service
- **Error handling**: Skips problematic ZIP codes and continues processing

---

## Output Example
| ZIP   | City      | State | County  | name                  | location        | distribution_type          | distance |
|-------|-----------|-------|---------|-----------------------|-----------------|-----------------------------|----------|
| 40003 | Bagdad    | KY    | Shelby  | MBM Corp-Frankfort    | Frankfort, KY   | Chain/Systems Distribution | 11 miles |
| 40004 | Bardstown | KY    | Nelson  | What Chefs Want       | Louisville, KY  | Specialized Foodservice     | 28 miles |

## Contributing
Feel free to fork this repository and submit a pull request with any improvements!

## License
This project is open-source and available under the MIT License.

## Author
andrepradika