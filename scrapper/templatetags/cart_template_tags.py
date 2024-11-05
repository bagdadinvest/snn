from django import template
from scrapper.models import ScrapedOrder

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = ScrapedOrder.objects.filter(user=user, ordered=False)
        if qs.exists():
            return sum(item.quantity for item in qs[0].items.all())
    return 0
