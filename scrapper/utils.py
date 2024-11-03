import os
import requests
from django.core.files.base import ContentFile
from django.core.files import File
from playwright.sync_api import sync_playwright
from .models import ScrapedItem, ScrapedItemImage
from bs4 import BeautifulSoup

def scrape_procsin_products():
    print("Starting the scraping process in headless mode...")
    scraped_data = []
    base_url = 'https://www.procsin.com'
    url = f"{base_url}/cilt-bakimi?ps=16&stock=1"  # Turkish version of the URL that loads all products

    with sync_playwright() as playwright:
        # Launch the browser in headless mode
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the Turkish page directly
        print(f"Navigating to URL: {url}")
        page.goto(url)
        print("Page loaded successfully.")

        # Wait for all product items to load
        print("Waiting for product items to load...")
        page.wait_for_selector(".product-item")

        # Count the total products on the page
        total_products = page.locator(".product-item").count()
        print(f"Total products found on the page: {total_products}")

        # Extract data for each product
        for index in range(total_products):
            print(f"\nExtracting product {index + 1} details...")
            product = page.locator(".product-item").nth(index)

            # Extract title, price, description, and image URL
            title = product.locator('.product-title').inner_text() if product.locator('.product-title').count() > 0 else None
            price_text = product.locator('.current-price .product-price').inner_text() if product.locator('.current-price .product-price').count() > 0 else None
            price = float(price_text.replace(' TL', '').replace(',', '.')) if price_text else None
            description_short = product.locator('.short-title div').inner_text() if product.locator('.short-title div').count() > 0 else None
            image_url = None
            picture_element = product.locator('picture.image-inner')
            if picture_element.count() > 0:
                image_url = picture_element.locator('img').get_attribute('src') if picture_element.locator('img').count() > 0 else None
                if image_url and image_url.startswith('/'):
                    image_url = f"{base_url}{image_url}"

            # Debugging: Confirm extraction of key details
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Description: {description_short}")
            print(f"Image URL: {image_url}")

            # Generate slug from title
            if title:
                slug = title.lower().replace(' ', '-').replace('.', '').replace(',', '')
            else:
                print(f"Warning: No title found for product {index + 1}. Skipping product.")
                continue

            # Construct the product URL
            url_suffix = product.locator('a.image-wrapper').get_attribute('href') if product.locator('a.image-wrapper').count() > 0 else None
            product_url = f"{base_url}{url_suffix}" if url_suffix else None

            # Add extracted data to the list
            scraped_data.append({
                'title': title,
                'price': price,
                'description_short': description_short,
                'image_url': image_url,
                'slug': slug,
                'product_url': product_url  # Store the constructed product URL
            })
            print(f"Product {index + 1} extracted: {title} with URL: {product_url} and Slug: {slug}")

        browser.close()
        print("Playwright scraping completed successfully.")

    # Step 2: Save each item to the database outside of the Playwright context
    for item in scraped_data:
        print(f"Saving product to database: {item['title']}")
        image_file = None
        if item['image_url']:
            image_response = requests.get(item['image_url'])
            if image_response.status_code == 200:
                image_file = ContentFile(image_response.content, name=f"{item['slug']}.jpg")

        # Save the product in the database, checking for existing slug to avoid duplicates
        ScrapedItem.objects.update_or_create(
            slug=item['slug'],
            defaults={
                'title': item['title'],
                'price': item['price'],
                'category': None,
                'description_short': item['description_short'],
                'image': File(image_file, name=f"{item['slug']}.jpg") if image_file else None,
                'is_active': True,
                'product_url': item['product_url']
            }
        )
        print(f"Product saved to database: {item['title']} with Slug: {item['slug']}")

    print("Scraping process completed.")


#########################################################################################################
################################### PICS DOWNLOAD #######################################################
#########################################################################################################

import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.files.base import ContentFile
from playwright.sync_api import sync_playwright
import requests
from .models import ScrapedItem, ScrapedItemImage

# Directory to save images within Django's media directory
base_output_dir = "media/items"

# List of valid image extensions
valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}

def fetch_image_data(img_url, idx, item_output_dir):
    """Download image and return Django file object."""
    try:
        response = requests.get(img_url)
        response.raise_for_status()

        # Save image locally
        image_path = os.path.join(item_output_dir, f"image_{idx + 1}.png")
        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)

        # Prepare image for Django
        with open(image_path, "rb") as file_content:
            django_file = ContentFile(file_content.read(), name=f"image_{idx + 1}.png")

        return django_file

    except Exception as e:
        print(f"[ERROR] Could not download or save image at {img_url}: {e}")
        return None

def download_images(page, item):
    """Downloads images from the product page and returns image data."""
    # Ensure the output directory for the item exists
    item_output_dir = os.path.join(base_output_dir, item.slug)
    os.makedirs(item_output_dir, exist_ok=True)
    print(f"[DEBUG] Created output directory for '{item.title}': {item_output_dir}")

    # Select gallery images
    all_images = page.query_selector_all('.product-images-gallery .swiper-slide img') + \
                 page.query_selector_all('.product-images-thumb .swiper-slide img')
    print(f"[DEBUG] Found {len(all_images)} images for '{item.title}'.")

    image_files = []
    for idx, img in enumerate(all_images[:12]):  # Limit to 12 images
        img_url = img.get_attribute('src')
        if img_url and any(img_url.lower().endswith(ext) for ext in valid_extensions):
            print(f"[DEBUG] Processing image {idx + 1}: {img_url}")
            django_file = fetch_image_data(img_url, idx, item_output_dir)
            if django_file:
                image_files.append(ScrapedItemImage(item=item, image=django_file))

    return image_files

def process_item(item):
    """Process a single item and collect its image data."""
    with sync_playwright() as p:
        print(f"[DEBUG] Starting Playwright session for '{item.title}'")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()
        page.goto(item.product_url)
        print(f"[DEBUG] Page loaded successfully for '{item.title}'")

        image_files = download_images(page, item)

        page.close()
        browser.close()
        print(f"[DEBUG] Playwright session complete for '{item.title}'")

    return image_files

def scrape_and_download_images():
    """Main function to scrape and download images for each item."""
    items = ScrapedItem.objects.filter(is_active=True)  # Filter for active items
    total_items = len(items)
    print(f"[DEBUG] Total items to process: {total_items}")

    all_image_entries = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_item, item): item for item in items}

        for future in as_completed(futures):
            item = futures[future]
            try:
                image_entries = future.result()
                all_image_entries.extend(image_entries)
                print(f"[DEBUG] Completed image processing for '{item.title}'")

                # Batch save images every 5 items
                if len(all_image_entries) >= 5:
                    ScrapedItemImage.objects.bulk_create(all_image_entries)
                    all_image_entries.clear()
                    print("[DEBUG] Batch of 5 images saved to the database")

            except Exception as exc:
                print(f"[ERROR] Exception processing '{item.title}': {exc}")

            # Introduce a random delay up to 20 seconds between each item batch
            delay = random.randint(1, 20)
            print(f"[DEBUG] Waiting {delay} seconds before processing the next batch")
            time.sleep(delay)

    # Save any remaining images
    if all_image_entries:
        ScrapedItemImage.objects.bulk_create(all_image_entries)
        print("[DEBUG] Final batch of images saved to the database")

    print("[DEBUG] All batches complete, image download process finished.")
