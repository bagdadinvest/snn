from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import re
from urllib.parse import urljoin

# Path to your ChromeDriver executable
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)

def sanitize_filename(filename):
    """
    Sanitize the filename to ensure it is valid for the file system.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_file(url, folder):
    """
    Download a file from a URL and save it to a specified folder.
    """
    response = requests.get(url)
    if response.status_code == 200:
        file_name = sanitize_filename(os.path.basename(url))
        file_path = os.path.join(folder, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded file: {file_path}')

def scrape_page(url):
    # Initialize the WebDriver
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the URL
        driver.get(url)

        # Wait for the page to fully load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
        )

        # Get the HTML content of the page
        page_html = driver.page_source

        # Save the HTML content to a file
        output_html_file_path = 'scraped_page.html'
        with open(output_html_file_path, 'w', encoding='utf-8') as file:
            file.write(page_html)

        print(f'Scraped HTML content saved to {output_html_file_path}')

        # Create directories for static files
        os.makedirs('css', exist_ok=True)
        os.makedirs('js', exist_ok=True)
        os.makedirs('images', exist_ok=True)

        # Extract and download CSS files
        css_links = [elem.get_attribute('href') for elem in driver.find_elements(By.CSS_SELECTOR, 'link[rel="stylesheet"]')]
        for link in css_links:
            full_url = urljoin(url, link)
            download_file(full_url, 'css')

        # Extract and download JS files
        js_links = [elem.get_attribute('src') for elem in driver.find_elements(By.CSS_SELECTOR, 'script[src]')]
        for link in js_links:
            full_url = urljoin(url, link)
            download_file(full_url, 'js')

        # Extract and download image files
        img_links = [elem.get_attribute('src') for elem in driver.find_elements(By.CSS_SELECTOR, 'img[src]')]
        for link in img_links:
            full_url = urljoin(url, link)
            download_file(full_url, 'images')

    finally:
        # Clean up and close the WebDriver
        driver.quit()
