from django import template
from django.utils.safestring import mark_safe
from scrapper.models import ScrapedItem  # Adjust if you introduce a new model

register = template.Library()

@register.simple_tag
def slides():
    items = ScrapedItem.objects.filter(is_active=True).order_by('pk')  # Adjust if using a specific model
    items_div = "".join(
        f"""<div class="item-slick1 item2-slick1" style="background-image: url(/media/{i.image});"><div class="wrap-content-slide1 sizefull flex-col-c-m p-l-15 p-r-15 p-t-150 p-b-170"><span class="caption1-slide1 m-text1 t-center animated visible-false m-b-15" data-appear="rollIn">{i.title}</span><h2 class="caption2-slide1 xl-text1 t-center animated visible-false m-b-37" data-appear="lightSpeedIn">{i.description_short}</h2><div class="wrap-btn-slide1 w-size1 animated visible-false" data-appear="slideInUp"><a href="{i.product_url}" class="flex-c-m size2 bo-rad-23 s-text2 bgwhite hov1 trans-0-4">Shop Now</a></div></div></div>"""
        for i in items
    )
    return mark_safe(items_div)
