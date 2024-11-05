from django.urls import path
from .views import (
    scraper_admin_panel, scrape_and_save_products,
    scrape_procsin_view, download_images_for_scraped_items_view,
    scraped_list_view, scraped_item_detail_view, scrape_product_skus_view
)
from . import views


urlpatterns = [
    path('admin-panel/', scraper_admin_panel, name='scraper_admin_panel'),  # Admin panel URL
    path('scrape-trendyol/', scrape_and_save_products, name='scrape_trendyol'),
    path('scrape-procsin/', scrape_procsin_view, name='scrape_procsin'),
    path('download-images/', download_images_for_scraped_items_view, name='download_images'),
    path('scrape-product-skus/', scrape_product_skus_view, name='scrape_product_skus'),  # New URL for SKU scraping
    path('', scraped_list_view, name='scraped_list'),
    path('item/<int:pk>/', scraped_item_detail_view, name='scrapeditem_detail'),
    path('create-product-page/<int:sku_id>/', views.create_product_page_view, name='create_product_page'),
]
