from django import template
from core.models import CartItem

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        items = CartItem.objects.filter(user=user, ordered=False)
        if items.exists():
            return items[0].item.count()
    else:
        return 0
