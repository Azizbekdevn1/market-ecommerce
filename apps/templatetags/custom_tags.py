from django.template import Library

from apps.models import WishList

register = Library()


@register.filter()
def has_wishlist(user_id, product_id):
    return WishList.objects.filter(user_id=user_id, product_id=product_id).exists()