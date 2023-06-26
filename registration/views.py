from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate, logout
from registration.forms import RegistrationForm,AccountAuthenticationForm
from django.contrib import messages
from .models import Account
from products.models import *
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control, never_cache

from django.conf import settings

from django.contrib.auth import get_user_model

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import RegistrationForm
from .utils import *
from django.utils.encoding import force_bytes, force_str
from django.db.models import Prefetch
from django.db.models import OuterRef, Subquery

from django.contrib import messages
from django.shortcuts import redirect
from .models import Account

import random
import string


from cart.models import *

# Create your views here.





# def index(request):
#     return render(request, 'base.html')
@never_cache
def home(request):
 
        return render(request,'home.html')
   

def generate_otp():
    digits = string.digits
    otp = ''.join(random.choice(digits) for _ in range(6))
    return otp


from .utils import generate_otp, send_otp

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")

    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

          
            otp_code = generate_otp() 
            send_otp(user.email, otp_code)  

            
            request.session['otp_code'] = otp_code
            request.session['email'] = user.email

           
            return redirect('verify_otp')

        else:
            context['registration_form'] = form

    return render(request, 'register.html', context)

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp_code')
        email = request.session.get('email')

        if entered_otp == saved_otp:
           
            user = Account.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(request, 'Congratulations! Your account is verified.')
            return redirect('home')
        else:
            
            messages.error(request, 'Invalid OTP code. Please try again.')

    return render(request, 'verify_otp.html')






def logout_view(request):
    request.session.flush()
    return redirect("home")




def login_view(request,*args,**kwargs):
    
    context ={}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    
    # destination = get_redirect_if_exist(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request,email = email, password = password)
            
            if user:
                login(request,user)
                request.session['email'] = email 
                return redirect("home")
        else:
        

            context['login_form'] = form

    # context['login_form'] = form
    return render(request,"login.html",context)


def shop(request):
    variants = Variant.objects.filter(is_listed=True)
    
    # Assign variant_id to the id attribute of each Variant
    for variant in variants:
        variant.variant_id = variant.uid
    
    context = {
        'variants': variants,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'store.html', context)


# def shop(request):
#     # variants = Variant.objects.filter(variis_listed=True)
#     variants = Variant.objects.filter(is_listed = True)
    

#     context = {
#         'variants': variants,
#         'MEDIA_URL': settings.MEDIA_URL,
#     }

#     return render(request, 'shop.html', context)

def productdetails(request, variant_id):
   
    product_details = Variant.objects.get(uid= variant_id)
    print("####################",variant_id)
    context ={
        'details' : product_details
        }
    return render(request ,"productpage.html", context )

 
