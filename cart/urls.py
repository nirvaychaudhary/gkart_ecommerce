from django.urls import path
from .views import *

app_name='cart'

urlpatterns = [
    path('', Cart_page, name='cart'),
    path('add_cart/<str:product_id>/', add_cart, name='add_cart'),
    path('decrease_cart/<str:product_id>/<str:cart_item_id>/', decrease_cart, name='decrease_cart'),
    path('remove_cart/<str:product_id>/<str:cart_item_id>/', remove_cart, name='remove_cart'),
    path('checkout/', Checkout, name='checkout'),

]