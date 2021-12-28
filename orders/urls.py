from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('place_order/',PlaceOrder, name='place_order'),
    path('payment',Payment, name='payment'),
]