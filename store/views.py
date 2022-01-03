from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def Store(request, category_slug=None):
    categories = None
    product_list = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        product_list = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(product_list, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = product_list.count()
    else:
        product_list = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(product_list, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.objects.count()
    context = {
        'Store_Title': 'Our Store',
        'product_list': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context=context) 

def Product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart = _cart_id(request), product = single_product).exists()
        # return HttpResponse(in_cart)
    except Exception as e:
        raise e
    context = {
        'title': 'Product Detail',
        'single_product': single_product,
        'in_cart': in_cart,

    }
    return render(request, 'store/product_detail.html', context=context)

def Search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product_list = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
            product_count = product_list.count()
    context = {
        'Search_Title': 'Search Results',
        'product_list': product_list,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context=context) 