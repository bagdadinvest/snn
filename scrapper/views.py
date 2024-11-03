import logging
from django.shortcuts import render
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
    print("Entered scraped_item_detail_view function.")  # Debug statement

    # Fetch the ScrapedItem object
    scraped_item = get_object_or_404(ScrapedItem, pk=pk)
    print(f"Fetched ScrapedItem with ID: {pk}, Title: {scraped_item.title}")  # Debug statement

    # Fetch related images for the ScrapedItem
    images = scraped_item.images.all()
    print(f"Fetched {images.count()} related images for ScrapedItem with ID: {pk}")  # Debug statement

    # Pass the ScrapedItem and related images to the template
    context = {
        'object': scraped_item,
        'images': images,
    }
    print("Rendering template with ScrapedItem and related images.")  # Debug statement

    return render(request, 'scrapeditem_detail.html', context)
