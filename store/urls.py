from django.urls import path
from .views import *

app_name='store'

urlpatterns = [
    path('', Store, name='store'),
    path('category/<slug:category_slug>/', Store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', Product_detail, name='product_detail'),
    path('search/', Search, name='search'),

]