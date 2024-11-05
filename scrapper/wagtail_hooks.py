from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import ProductSku

class ProductSkuAdmin(ModelAdmin):
    model = ProductSku
    menu_label = "Product SKUs"
    menu_icon = "tag"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "sku", "price")
    search_fields = ("title", "sku")

modeladmin_register(ProductSkuAdmin)

@hooks.register('register_admin_menu_item')
def register_scraper_admin_menu_item():
    return MenuItem(
        _('Scraper Admin Panel'),  # Menu label, with translation support
        reverse('scraper_admin_panel'),  # URL name registered in the `scrapper/urls.py`
        classnames='icon icon-folder-open-inverse',  # Choose an appropriate icon
        order=2000  # Position in the menu
    )
