from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("<slug:category_slug>/", views.store, name="selected_category"),
    path("<slug:category_slug>/<slug:product_slug>/", views.product_detail, name="single_product"),
]
