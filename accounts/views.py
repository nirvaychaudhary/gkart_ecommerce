from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import RegistrationForm

# '''email verification import'''
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes

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
            auth.login(request, user)
            messages.success(request, "Login Sucessful.")
            return redirect('accounts:dashboard')     
        else:
            messages.success(request, "Email or Password Incorrect!")
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

@login_required(login_url='accounts:login')
def Dashboard(request):
    return render(request, 'accounts/dashboard.html')