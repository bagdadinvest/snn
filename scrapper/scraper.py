# scraper/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import os

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Path to chromedriver
    CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    service = Service(CHROMEDRIVER_PATH)

    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_page(url):
    driver = initialize_driver()
    driver.get(url)

    # Get HTML content
    html_content = driver.page_source
    html_path = Path('scrapper/templates/scraped_page.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    driver.quit()
