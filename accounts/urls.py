from django.urls import path
from .views import *

app_name='accounts'

urlpatterns = [
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('', Dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', Activate, name='activate'),
]