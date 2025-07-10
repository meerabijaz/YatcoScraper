# YatcoScraper

# Yatco.com Business Directory Scraper

This Python project implements a web scraper using Selenium to extract business listings from the Yatco.com Business Directory. It automates browsing through multiple pages of listings, collects relevant business details, and saves the structured data into a CSV file.

## Features

* Data Extraction: Collects key details such as Business Name, Business Link, Categories, Location, and Description from each business card on the directory pages.
* Pagination Support: Automatically navigates through a user-specified number of pages to gather comprehensive data.
* Data Cleaning: Extracts and normalizes text content by trimming whitespace and handling missing fields gracefully.
* Error Handling: Manages timeouts and missing elements robustly to ensure smooth scraping across pages.
* CSV Export: Outputs the collected data into a well-structured CSV file under a dedicated `data/` folder.
* Logging: Prints progress and error messages to the console for easy monitoring during the scraping process.

## Usage

1. Run the script.
2. Enter the number of pages you want to scrape when prompted.
3. The scraper will visit each page, extract business information, and save it into `data/yatco_business_data.csv`.
4. Monitor console output for scraping status and any potential warnings.

## Dependencies

* Python 3.x
* Selenium
* A compatible ChromeDriver executable installed and available in PATH


