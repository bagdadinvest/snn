from django.urls import path
from .views import scrape_and_save_products, scrape_procsin_view, download_images_for_scraped_items_view, scraped_list_view, scraped_item_detail_view

urlpatterns = [
    path('xx', scrape_and_save_products, name='scrape_trendyol'),
    path('scrape-procsin/', scrape_procsin_view, name='scrape_procsin'),
    path('download-images/', download_images_for_scraped_items_view, name='download_images'),
    path('', scraped_list_view, name='scraped_list'),
    path('item/<int:pk>/', scraped_item_detail_view, name='scrapeditem_detail'),  # Updated URL pattern for item detail view
]
