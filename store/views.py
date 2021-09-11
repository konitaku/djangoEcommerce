from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id


# Create your views here.
def store(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        products_count = products.count()

    else:
        products = Product.objects.filter(is_available=True)
        products_count = products.count()

    context = {
        "products": products,
        "products_count": products_count,
        "request": request
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug=None, product_slug=None):
    # product = get_object_or_404(Product, slug=product_slug, is_available=True)

    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        is_in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e

    context = {
        "product": product,
        "is_in_cart": is_in_cart,
    }
    return render(request, "store/product-detail.html", context)
