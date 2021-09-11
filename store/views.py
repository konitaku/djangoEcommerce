from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from functools import reduce
from operator import and_, or_


def paginate_query(request, queryset, count):
    """
    :param request: Request Object
    :param queryset: Item Objects List
    :param count: Number of Items Per Page
    :return: Page Object
    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)
    return paged_products


# Create your views here.
def store(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True).order_by("-id")
        products_count = products.count()

    else:
        products = Product.objects.filter(is_available=True).order_by("-id")
        products_count = products.count()

    paged_products = paginate_query(request, products, settings.NUMBER_OF_ITEMS_PER_PAGE)
    num_of_items = len(paged_products.object_list)

    context = {
        # "products": products,
        "products": paged_products,
        "products_count": products_count,
        "num_of_items": num_of_items,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug=None, product_slug=None):
    # product = get_object_or_404(Product, slug=product_slug, is_available=True)

    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        is_in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except ObjectDoesNotExist:
        return redirect("store")

    context = {
        "product": product,
        "is_in_cart": is_in_cart,
    }
    return render(request, "store/product-detail.html", context)


def search(request):
    keyword: str
    keyword = request.GET.get("keyword")
    if keyword:
        # 検索キーワードから半角・全角スペースを除外
        # exclusion_list = {" ", "　"}  # set型のオブジェクト
        # formatted_keyword = [char for char in keyword if char not in exclusion_list]
        formatted_keyword = keyword.split()

        # 整形したキーワードについて1文字ずつクエリを作成し、それらを１つに合成（AND検索)
        query_list = [Q(product_name__icontains=word) | Q(description__icontains=word) for word in formatted_keyword]
        query = reduce(or_, query_list)

        # 作成したクエリを実行
        products = Product.objects.filter(query).order_by("-id")

        products_count = products.count()
        paged_products = paginate_query(request, products, settings.NUMBER_OF_ITEMS_PER_PAGE)
        num_of_items = len(paged_products.object_list)
    else:
        return redirect("store")

    context = {
        "products": paged_products,
        "products_count": products_count,
        "num_of_items": num_of_items,
        "keyword": "+".join(keyword.split()),
    }
    return render(request, "store/store.html", context)
