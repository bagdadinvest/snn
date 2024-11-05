import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .trendyol_scraper import scrape_trendyol_products
from scrapper.models import ScrapedItem
from .utils import scrape_procsin_products, scrape_and_download_images
import threading
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)

def scrape_and_save_products(request):
    logger.debug("Starting scrape_and_save_products function.")
    if request.method == 'POST':
        url = request.POST.get('url')
        max_products = 50  # Default value

        if url:
            logger.debug(f"Scraping URL: {url}")
            try:
                products = scrape_trendyol_products(url, max_products=max_products)

                # Saving each product to the database with `product_url`
                for product in products:
                    ScrapedItem.objects.create(
                        brand=product['brand'],
                        title=product['name'],
                        price=product['price'],
                        image=product['image_url'],
                        link=product['link'],
                        product_url=product['link']  # Ensure product URL is saved
                    )
                logger.info(f"Successfully saved {len(products)} products to the database.")
                return JsonResponse({'status': 'success', 'message': f'Scraped and saved {len(products)} products.'})
            except Exception as e:
                logger.error(f"Error while scraping or saving products: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'scrape_form.html')

def scrape_procsin_view(request):
    # Run the scraping function in a separate thread
    scraping_thread = threading.Thread(target=scrape_procsin_products)
    scraping_thread.start()
    scraping_thread.join()  # Wait for thread to complete (optional; you can remove if not needed)

    return JsonResponse({'status': 'success', 'message': 'Products scraped and saved successfully.'})

def download_images_for_scraped_items_view(request):
    """
    View to initiate the image download process for all scraped items.
    Calls the download_images_for_scraped_items function from utils.py.
    """
    try:
        scrape_and_download_images()
        response = {
            'status': 'success',
            'message': 'Image download process completed successfully.'
        }
    except Exception as e:
        logger.error(f"Error during image download: {e}")
        response = {
            'status': 'error',
            'message': f"An error occurred during the image download process: {str(e)}"
        }

    return JsonResponse(response)


def scraped_list_view(request):
    """
    View to display all scraped items along with their images.
    This view can also serve as an API endpoint for infinite scroll.
    """
    scraped_items = ScrapedItem.objects.prefetch_related('images').all()

    # For AJAX requests (infinite scroll)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page_number = request.GET.get('page', 1)
        paginator = Paginator(scraped_items, 12)  # Show 12 items per page
        page_obj = paginator.get_page(page_number)

        items = []
        for item in page_obj:
            item_data = {
                'title': item.title,
                'price': item.price,
                'url': item.get_absolute_url(),
                'image_url': item.images.first().image.url if item.images.exists() else None
            }
            items.append(item_data)

        return JsonResponse({
            'items': items,
            'has_next': page_obj.has_next()
        })

    # For normal rendering
    paginator = Paginator(scraped_items, 12)  # Show 12 items per page
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'scrapped_list.html', {
        'object_list': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })



def scraped_item_detail_view(request, pk):
    print("DEBUG: Entered scraped_item_detail_view function.")  # Initial entry
    try:
        # Fetch the ScrapedItem object
        scraped_item = get_object_or_404(ScrapedItem, pk=pk)
        print(f"DEBUG: Fetched ScrapedItem with ID: {pk}, Title: {scraped_item.title}")
    except Exception as e:
        print(f"ERROR: Failed to fetch ScrapedItem with ID: {pk} - {e}")
        return JsonResponse({'error': 'ScrapedItem not found'}, status=500)

    try:
        # Fetch related images for the ScrapedItem
        images = scraped_item.images.all()
        print(f"DEBUG: Fetched {images.count()} related images for ScrapedItem with ID: {pk}")
    except Exception as e:
        print(f"ERROR: Failed to fetch images for ScrapedItem ID: {pk} - {e}")
        return JsonResponse({'error': 'Error fetching images'}, status=500)

    # Preparing context data for the template
    context = {
        'object': scraped_item,
        'images': images,
    }
    print("DEBUG: Context data prepared. About to render template.")

    # Render the template with the scraped item and images
    try:
        response = render(request, 'scrapeditem_detail.html', context)
        print("DEBUG: Template rendered successfully.")
        return response
    except Exception as e:
        print(f"ERROR: Template rendering failed - {e}")
        return JsonResponse({'error': 'Template rendering error'}, status=500)


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def scraper_admin_panel(request):
    return render(request, 'scraper_admin_panel.html')

from django.http import JsonResponse
from .utils import scrape_and_create_product_skus  # Assuming this function is in utils.py
import threading

def scrape_product_skus_view(request):
    """
    View to initiate the SKU scraping and saving process.
    Runs in a separate thread to prevent blocking.
    """
    if request.method == 'POST':
        # Start the scraping process in a separate thread
        scraping_thread = threading.Thread(target=scrape_and_create_product_skus)
        scraping_thread.start()

        return JsonResponse({
            'status': 'success',
            'message': 'SKU scraping process has been started successfully.'
        })
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method. Please use POST.'
    })

# In views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import ProductSku
from .utils import create_product_page_from_sku

def create_product_page_view(request, sku_id):
    """
    View to create a ProductPage from a given SKU.
    """
    # Get the ProductSku instance by ID or return a 404 if not found
    sku_instance = get_object_or_404(ProductSku, id=sku_id)

    # Call the function to create the ProductPage
    try:
        create_product_page_from_sku(sku_instance)
        return JsonResponse({"status": "success", "message": f"ProductPage created for SKU '{sku_instance.sku}'."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
