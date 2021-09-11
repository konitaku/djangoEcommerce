from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add-cart/<int:product_id>/", views.add_cart_item, name="add_cart"),
    path("sub-cart/<int:product_id>/", views.sub_cart_item, name="sub_cart"),
    path("remove-cart/<int:product_id>/", views.remove_cart_item, name="remove_cart"),
]
