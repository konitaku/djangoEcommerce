from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import Product
from .models import Cart, CartItem


# Create your views here.
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    try:
        cart_obj = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart_obj = Cart.objects.create(cart_id=_cart_id(request))
        cart_obj.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart_obj)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart_obj, quantity=1)
    cart_item.save()
    return redirect("cart")


def sub_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    try:
        cart_obj = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart_obj)
    except Cart.DoesNotExist:
        pass  # Just Ignore
    else:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect("cart")


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    try:
        cart_obj = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart_obj)
    except Cart.DoesNotExist:
        pass  # Just Ignore
    else:
        cart_item.delete()
    return redirect("cart")


def cart(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_obj = None
    cart_items = None

    try:
        cart_obj = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_obj, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (10 * total) / 100
        grand_total = total + tax

    except Cart.DoesNotExist:
        pass  # Just Ignore

    context = {
        "cart": cart_obj,
        "cart_items": cart_items,
        "total": total,
        "quantity": quantity,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "store/cart.html", context)
