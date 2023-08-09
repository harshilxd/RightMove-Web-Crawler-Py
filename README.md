# Real Estate Scraper

This Python script provides a robust and efficient way to scrape property information from `rightmove.co.uk`. Designed to handle multiple URLs, it fetches a wealth of details about a property, such as title, description, price, address, and many more.

## Features

- **Asynchronous Fetching**: Utilizes asynchronous programming paradigms for web requests, ensuring faster data retrieval across multiple URLs.
- **Detailed Property Info**: Captures comprehensive details of properties including availability status, property type, features, etc.
- **Browser-like Headers**: Employs headers mimicking regular browser requests to reduce chances of getting blocked.
- **Parsed Output**: Transforms raw web data into a structured and more readable JSON format.
- **Error Handling**: Gracefully manages scenarios where expected data isn't available on a page.

## Setup & Installation

1. **Python**:
   - Ensure Python 3.8 or newer is installed.
   
2. **Dependencies**:
   - Install the required Python libraries with:
     ```
     pip install httpx parsel jmespath
     ```

## Usage

1. **URLs**:
   - Modify the URLs list in the script if you desire to scrape other property links.
   
2. **Execution**:
   - Run the script via:
     ```
     python <script_name>.py
     ```
   Replace `<script_name>.py` with the filename you've designated for the script.
   
3. **Output**:
   - Post execution, the scraped data gets stored in `estate_data.json`.

## Contributing

Contributions are welcome! Fork the project and submit enhancements or fixes through pull requests.

## Caution

Remember, web scraping may violate terms of service on some sites. Always verify your right to scrape a website and ensure adherence to its robots.txt or terms of service.

## License

This project is open-sourced. Ensure to give appropriate attribution if you utilize or adapt this code for your endeavors.
