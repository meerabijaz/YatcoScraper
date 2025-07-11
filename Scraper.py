# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
from datetime import datetime

# Output file name
output_file = "yatco_business_data.csv"

# Create a 'data' directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Define the CSV headers
headers = [
    "Business_Name",
    "Business_Link",
    "Business_Categories",
    "Business_Location",
    "Business_Description",
    "Page_Number",
    "Scraped_At"
]

# Ask user how many pages they want to scrape
num_pages = int(input("How many pages do you want to scrape? "))

# Launch Chrome browser
driver = webdriver.Chrome()

# Open the CSV file to write data
with open(os.path.join("data", output_file), mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)  # Write the header row

    # Loop through each page
    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}...")

        # Construct the URL for the current page
        url = (
            f"https://www.yatco.com/business-services/?sort=1&pagination=1"
            f"&page_index={page}&page_size=12&status=1&records=12"
            f"&has_been_processed=true&isActive=true&page={page}"
        )
        driver.get(url)  # Load the page

        # Wait until all business cards are loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.col-service'))
            )
        except:
            print(f" Timeout while waiting for cards on page {page}")
            continue  # Skip to the next page if timeout

        # Find all business service cards on the page
        cards = driver.find_elements(By.CSS_SELECTOR, 'div.col-service')

        # Extract data from each card
        for card in cards:
            # Initialize default values
            business_name = ""
            business_link = ""
            business_categories = ""
            business_location = ""
            business_description = ""

            # Try extracting the business name and link
            try:
                name_link_el = card.find_element(By.CSS_SELECTOR, "h3 a")
                business_name = name_link_el.text.strip()
                business_link = name_link_el.get_attribute("href")
            except Exception as e:
                print(f"Could not get name/link: {e}")

            # Try extracting the category, location, and description
            try:
                p_elements = card.find_elements(By.CSS_SELECTOR, "div.info_ser p")
                locations = []

                for p in p_elements:
                    try:
                        # Check if <p> has any icons/images to identify field type
                        img_elements = p.find_elements(By.TAG_NAME, "img")
                        if img_elements:
                            img_alt = img_elements[0].get_attribute("alt").lower()
                            img_src = img_elements[0].get_attribute("src").lower()

                            # Extract text content inside the paragraph
                            text_elements = p.find_elements(By.CSS_SELECTOR, "span.service-result-text")
                            if text_elements:
                                text = text_elements[0].text.strip()

                                # Identify and assign based on icon type
                                if "categories" in img_alt or "categories_icon" in img_src:
                                    business_categories = text
                                elif "map-pin" in img_alt or "map-pin" in img_src:
                                    locations.append(text)
                                elif "globe" in img_alt or "globe" in img_src:
                                    locations.append(text)
                                elif "message" in img_alt or "about" in img_alt or "message-square" in img_src:
                                    business_description = text
                        else:
                            # Handle text directly inside <p> (no icon)
                            p_text = p.text.strip()
                            if p_text and len(p_text) > 50:  # Likely a description
                                business_description = p_text

                    except Exception as inner_e:
                        print(f"Error processing paragraph: {inner_e}")
                        continue

                # Combine multiple location parts if available
                business_location = ", ".join(locations)

            except Exception as e:
                print(f"Could not get categories/location/description: {e}")

            # Timestamp of scraping
            scraped_at = datetime.now().strftime("%d/%m/%Y %H:%M")

            # Write the extracted data to the CSV
            writer.writerow([
                business_name,
                business_link,
                business_categories,
                business_location,
                business_description,
                page,
                scraped_at
            ])

            # Optional: print to console for progress tracking
            print(f"Extracted: {business_name} | {business_categories} | {business_location}")

# Close the browser after scraping is complete
driver.quit()

# Final message
print(f"Scraped data from {num_pages} pages and saved to 'data/{output_file}'")
