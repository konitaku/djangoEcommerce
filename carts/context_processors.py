from .models import Cart, CartItem
from .views import _cart_id


def cart_counter(request):
    count = 0
    if "admin" in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                count += cart_item.quantity
        except Cart.DoesNotExist:
            pass
        return dict(cart_count=count)
