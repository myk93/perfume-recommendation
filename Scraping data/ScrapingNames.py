import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Initialize the WebDriver for Edge
driver = webdriver.Edge()
driver.get('https://www.wikiparfum.com/en/fragrances')


# Function to extract fragrance names and URLs from the current page
def extract_fragrance_names_and_urls():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    fragrances = []

    # Find all a tags with the specific href pattern
    for a_tag in soup.select('a[href*="/en/fragrances/"]'):
        url = "https://www.wikiparfum.com" + a_tag['href']

        # The corresponding name should be within the h6 tag inside the parent div
        name_tag = a_tag.select_one('h6.font-secondary.uppercase.text-h6Primar')
        if name_tag:
            name = name_tag.get_text()
            fragrances.append({"name": name, "webPage": url})

    return fragrances


# Wait for the initial fragrances to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h6.font-secondary.uppercase.text-h6Primar')))
time.sleep(10)  # Adjust the sleep time as necessary

all_fragrances = extract_fragrance_names_and_urls()

while True:
    try:
        # Find and click the "Load more" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, 'button.text-center.text-gold800')
        driver.execute_script("arguments[0].click();", load_more_button)

        # Wait for new fragrances to load
        time.sleep(8)

        new_fragrances = extract_fragrance_names_and_urls()
        all_fragrances.extend(new_fragrances)

    except Exception as e:
        print(f"No more fragrances found or an error occurred: {e}")
        break

# Remove duplicates
unique_fragrances = {v['name']: v for v in all_fragrances}.values()
driver.quit()

with open('names.json', 'w', encoding="utf-8") as json_file:
    json.dump(list(unique_fragrances), json_file, indent=4, ensure_ascii=False)
