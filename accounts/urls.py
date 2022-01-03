from django.urls import path
from .views import *

app_name='accounts'

urlpatterns = [
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('forgotpassword/', ForgotPassword, name='forgotpassword'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('', Dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', Activate, name='activate'),
    path('reset_password/<uidb64>/<token>/', resetpassword_validate, name='reset_password_validate'),
    path('reset_password/', ResetPassword, name='reset_password'),
]