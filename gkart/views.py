from django.shortcuts import render

from store.models import Product

def Homepage(request):
    product_list = Product.objects.all().filter(is_available=True)
    context = {
        'Title': 'Products',
        'product_list': product_list
    }
    return render(request, 'home.html', context=context)