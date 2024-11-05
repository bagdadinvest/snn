from django import template
from django.utils.safestring import mark_safe
from scrapper.models import ScrapedCategory

register = template.Library()

@register.simple_tag
def categories():
    items = ScrapedCategory.objects.filter(is_active=True).order_by('title')
    items_li = "".join(
        f"""<li><a href="/category/{i.slug}">{i.title}</a></li>"""
        for i in items
    )
    return mark_safe(items_li)

@register.simple_tag
def categories_mobile():
    items = ScrapedCategory.objects.filter(is_active=True).order_by('title')
    items_li = "".join(
        f"""<li class="item-menu-mobile"><a href="/category/{i.slug}">{i.title}</a></li>"""
        for i in items
    )
    return mark_safe(items_li)

# Additional functions can follow the same pattern.
