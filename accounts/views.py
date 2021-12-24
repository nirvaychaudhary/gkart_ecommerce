from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .models import Account
from .forms import RegistrationForm

# '''email verification import'''
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from cart.views import _cart_id
from cart.models import CartItem, Cart
import requests

def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name'] 
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number'] 
            password = form.cleaned_data['password'] 
            username = email.split("@")[0].lower()
            # print("Username is ::: ", username)
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            # '''user activation'''
            current_site = get_current_site(request)
            mail_subject = "Please Activate Your Account"
            message = render_to_string("accounts/account_verification_email.html", {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, "Account has registered sucessfully")
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'title': 'Registration Form',
        'form': form,
    }
    return render(request, 'accounts/register.html', context=context)

def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                print("cart::: ",Cart.objects.all())
                cart = Cart.objects.get(cart = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                print("cart item exists::: ", is_cart_item_exists)
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []

                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    cart_item = CartItem.objects.filter(user=user)
                '''
                existing variations => getting from database
                current variation => getting from product variation list
                item_id => getting from database
                '''
                ex_var_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                
                for pr in product_variation:
                    if pr in ex_var_list:
                        index = ex_var_list.index(pr)
                        item_id = id[index]
                        item = CartItem.objects.get(id=item_id)
                        item.quantity += 1
                        item.user = user
                        item.save()
                    else:
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user = user
                            item.save()

            except:
                pass
        
            auth.login(request, user)
            messages.success(request, "Login Sucessful.")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print("query::: ", query)
                params = dict(x.split("=") for x in query.split('&'))
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)     

            except:
                return redirect('accounts:dashboard')     

        else:
            messages.error(request, "Email or Password Incorrect!")
            return redirect('accounts:login') 

    return render(request, 'accounts/login.html')

@login_required(login_url='accounts:login')
def Logout(request):
    auth.logout(request)
    messages.success(request, 'Logout Sucessful.')
    return redirect('accounts:login')

def Activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account Activated successfully!')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid Account Activation Link!')
        return redirect('accounts:register')

def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # forgot password 
            current_site = get_current_site(request)
            mail_subject = "Password Reset"
            message = render_to_string("accounts/reset_email_password.html", {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Password reset email has sent to your email address.")
            return render(request, 'accounts/forgotpassword.html')
        else:
            messages.error(request,'Email does not exists!')
            return redirect('accounts:forgotpassword')
    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Please reset your password!')
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'link expired!')
        return redirect('accounts:login')

def ResetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            try:
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password Sucessfully Reset')
                return redirect('accounts:login')
            except Exception as e:
                print('e as error::: ', e)
                raise e
                
        else:
            messages.error(request, 'password does not match!')
            return redirect('accounts:reset_password')
    else:
        return render(request, 'accounts/reset_password.html')

@login_required(login_url='accounts:login')
def Dashboard(request):
    return render(request, 'accounts/dashboard.html')