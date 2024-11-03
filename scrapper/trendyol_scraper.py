from playwright.sync_api import sync_playwright
import time

def scrape_trendyol_products(url, max_products=50):
    products = []

    with sync_playwright() as p:
        print("[DEBUG] Starting Playwright")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        print(f"[DEBUG] Navigating to URL: {url}")
        page.goto(url)

        previous_product_count = 0

        while len(products) < max_products:
            print(f"[DEBUG] Current product count: {len(products)}")

            # Wait for products to load after scrolling
            product_elements = page.query_selector_all(".p-card-wrppr")
            new_product_count = len(product_elements)
            print(f"[DEBUG] Found {new_product_count} product elements on the page")

            if new_product_count > previous_product_count:
                print("[DEBUG] New products loaded, updating count")
                previous_product_count = new_product_count
            else:
                # Scroll down if no new products have loaded
                print("[DEBUG] No new products loaded, scrolling down")
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                time.sleep(5)

            print(f"[DEBUG] Extracting details from {len(product_elements)} product elements")

            for product_element in product_elements:
                try:
                    # Extract brand
                    brand_element = product_element.query_selector(".prdct-desc-cntnr-ttl")
                    brand = brand_element.inner_text() if brand_element else "N/A"

                    # Extract main and sub product name
                    name_main_element = product_element.query_selector(".prdct-desc-cntnr-name.hasRatings")
                    name_sub_element = product_element.query_selector(".product-desc-sub-text")
                    name_main = name_main_element.inner_text() if name_main_element else ""
                    name_sub = name_sub_element.inner_text() if name_sub_element else ""
                    name = f"{name_main} {name_sub}".strip() or "N/A"

                    # Extract price
                    price_element = product_element.query_selector(".prc-box-dscntd") or product_element.query_selector(".prc-box-sllng")
                    price = price_element.inner_text() if price_element else "N/A"

                    # Extract image URL
                    image_element = product_element.query_selector(".p-card-img-wr img")
                    image_url = image_element.get_attribute("src") if image_element else "N/A"

                    # Extract link
                    link_element = product_element.query_selector(".prdct-desc-cntnr-ttl a")
                    link = link_element.get_attribute("href") if link_element else "N/A"
                    full_link = f"https://www.trendyol.com{link}" if link else "N/A"

                    print(f"[DEBUG] Product extracted: Brand: {brand}, Name: {name}, Price: {price}, Image URL: {image_url}, Link: {full_link}")

                    products.append({
                        "brand": brand,
                        "name": name,
                        "price": price,
                        "image_url": image_url,
                        "link": full_link
                    })
                except Exception as e:
                    print(f"[ERROR] Failed to extract product details: {e}")

                # Stop if we've reached the maximum number of products
                if len(products) >= max_products:
                    print(f"[DEBUG] Reached max product limit: {max_products}")
                    break

        print("[DEBUG] Closing browser")
        browser.close()

    print(f"[DEBUG] Total products scraped: {len(products)}")
    return products

# Example usage
if __name__ == "__main__":
    url = "https://www.trendyol.com/procsin-x-b101963"
    scraped_products = scrape_trendyol_products(url)
    print("[DEBUG] Scraped Products:")
    for product in scraped_products:
        print(product)
