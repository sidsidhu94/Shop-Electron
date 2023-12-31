from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login,authenticate, logout
from registration.forms import RegistrationForm,AccountAuthenticationForm
from django.contrib import messages
from registration.models import Account
from userprofile.models import Wallet
from checkout.models import Order,Orderitem
import decimal
from decimal import Decimal
from products.models import *
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control, never_cache
from django.utils.dateparse import parse_date
import datetime
from django.utils import timezone
from django.conf import settings
from django.db.models import Count,Sum

from django.contrib.auth import get_user_model

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.db.models import Prefetch
from django.db.models import OuterRef, Subquery

from django.contrib import messages
from django.shortcuts import redirect
# from .models import Account

import random
import string

# Create your views here.
@cache_control(on_cache = True, must_revalidate = True, no_store = True)

def admin_login(request):
    if 'admin' in request.session:
        return redirect('dashboard')
  
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_superuser:
                request.session['admin'] = username
                login(request, user)
                return redirect('dashboard')
                
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('admin_login')

        else:


            return render(request, 'admin_login.html')

@never_cache    
def dashboard(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
        total_orders = orders.count()
        orders    = Order.objects.all().order_by('-id')
        total_sales = orders.aggregate(Sum('total_price'))['total_price__sum']
        
        today = timezone.now().date()
        daily_orders = Order.objects.filter(created_at__date=today).values('status').annotate(num_orders=Count('id')).order_by('status')
        orders_today = daily_orders.aggregate(total_orders=Sum('num_orders'))['total_orders']
        today_sales = daily_orders.aggregate(Sum('total_price'))['total_price__sum']

        # print(orders_today)
      
        return render(request,'dashboard.html',locals())
    else:
        return redirect('admin_login')
    
def admin_logout(request):
    if 'admin' in request.session:
        request.session.flush()
    logout(request)
    return redirect('admin_login')
        
 ######################### USER SIDE  #########################       
    
def user(request):
        user = Account.objects.filter(is_staff = False)

        paginator = Paginator(user, 10)
        page_number = request.GET.get('page')
        paginated_users = paginator.get_page(page_number)
        context = {
            'users': paginated_users,
            'paginated_users': paginated_users,
        }

        # context ={
        #     'user' : user,
            
        # }
        return render(request, 'user.html',context)


def block_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('user')

def unblock_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('user')


 ######################### CATEGORY  #########################    

def category(request):
    categories = Category.objects.all().order_by('uid')
    context = {
        'categories': categories
        }
    return render(request, 'category.html', context)

def list_category(request, category_id):
    category = Category.objects.get(uid=category_id)
    category.is_listed = True
    category.save()
    
    return redirect('category')

def unlist_category(request, category_id):
    category = Category.objects.get(uid=category_id)
    category.is_listed = False
    category.save()
    
    return redirect('category')


def delete_category(request,category_id):
    category = Category.objects.get(uid=category_id)
    category.delete()
    

    return redirect('category')


def update_category(request, category_id):
    category = Category.objects.get(uid=category_id)
    

    if request.method == "POST":
        
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')

        category.category_name = category_name
        category.category_image = category_image
        category.save()

        return redirect('category') 

    context = {
        'category': category
    }

    return render(request, 'category.html', context)

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
       
        category_image = request.FILES.get('category_image')
        

            

        category = Category(category_name=category_name, category_image=category_image)
        category.save()

        return redirect('category')

    return render(request, 'addcategory.html')




def base(request):
    return render(request,'base.html')

 ######################### PRODUCTS  #########################    

def product(request):
    products = Product.objects.all().order_by('uid')
    categories = Category.objects.all()
    context = {
        'products': products,'categories': categories
        }
    return render(request, 'product.html', context)



def add_products(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category_name')
        product_description = request.POST.get('prodct_description')
        image       =  request.FILES.get('image')
        

        
        product = Product.objects.create(
            Product_name=product_name,
            category=Category.objects.get(category_name=category_id,),
            prodct_description=product_description,
            image = image
        )

       
        
        
        return redirect('product')
    
    
    categories = Category.objects.filter(is_listed= True)
    
    return render(request, 'add_products.html', {'categories': categories})

def list_product(request, product_id):
    product = Product.objects.get(uid=product_id)
    product.is_listed = True
    product.save()
    
    return redirect('product')

def unlist_product(request, product_id):
    product = Product.objects.get(uid=product_id)
    product.is_listed = False
    product.save()
    
    return redirect('product')

def update_product(request,product_id):
    product = Product.objects.get(uid = product_id)
    categories = Category.objects.all()
    
    if request.method == "POST":
        product_name = request.POST.get('Product_name')
        
        prodct_description = request.POST.get('prodct_description')
        image = request.FILES.get('image')

        product.Product_name = product_name
        product.prodct_description = prodct_description
        product.image = image
        product.save()

        return redirect('product') 

    context = {
        'product': product
    }

    return render(request, 'product.html', context)



 ######################### VARIANTS  #########################    

def variants(request):
    
    variants = Variant.objects.all()
    categories = Category.objects.all()
    context = {
        'variants': variants,'categories': categories
        }
    return render(request,'variants.html', context)

def add_variants(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')
        color_id = request.POST.get('color')
        storage_id = request.POST.get('memory')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        images = request.FILES.getlist('images')

        # Perform validation
        if not product_id or not color_id or not storage_id or not price or not quantity or not images:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('add_variants')  

        try:
            product = Product.objects.get(Product_name=product_id)
            color = Color.objects.get(color_name=color_id)
            storage = Storage.objects.get(memory=storage_id)
        except (Product.DoesNotExist, Color.DoesNotExist, Storage.DoesNotExist):
            messages.error(request, 'Invalid product, color, or storage.')
            return redirect('add_variants')  

        if int(quantity) < 0 or float(price) < 0:
            messages.error(request, 'Quantity and price cannot be negative.')
            return redirect('add_variants')  
        # Save the variant
        variant = Variant(
            product=product,
            color=color,
            storage=storage,
            price=price,
            quantity=quantity,
        )
        variant.save()

        variant_name = variant.variant_name
        for img in reversed(images):
            image = VariantImage.objects.create(
                variant=Variant.objects.get(variant_name=variant_name),
                image=img,
            )

        return redirect('variants')  

    products = Product.objects.all()
    colors = Color.objects.all()
    storages = Storage.objects.all()
    screensizes = Screensize.objects.all()
    context = {
        'products': products,
        'colors': colors,
        'storages': storages,
        'screensizes':screensizes,
    }
    return render(request, 'add_variants.html', context)


def list_variants(request, variants_id):
    variant = Variant.objects.get(uid=variants_id)
    variant.is_listed = True
    variant.save()
    
    return redirect('variants')

def unlist_variants(request, variants_id):
    variant = Variant.objects.get(uid=variants_id)
    variant.is_listed = False
    variant.save()
    
    return redirect('variants')

def update_variants(request,variants_id):
    variants = Variant.objects.get(uid = variants_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        
        variants.price = price
        variants.quantity = quantity
        variants.save()
        

        return redirect('variants') 

    context = {
        'variants': variants
    }

    return render(request, 'variant.html', context)


 ######################### COLOR  #########################    

def color(request):
    colors = Color.objects.all()
    context = {
        'colors': colors
    }

    return render(request,'color.html', context)

def add_color(request):
    if request.method == 'POST':
        color_name = request.POST.get('color_name')
        color_code = request.POST.get('color_code')
        if color_name:
            color = Color(color_name=color_name,color_code=color_code)
            color.save()
            return redirect('color') 
    return render(request, 'add_color.html')


 ######################### STORAGE  #########################    

def storage(request):
    storages = Storage.objects.all()
    context = {
        'storages':storages
    }
    return render(request,'storage.html', context)


def add_storage(request):
    if request.method == 'POST':
        memory = request.POST.get('memory')

        if memory:
            storage = Storage(memory=memory)
            storage.save()
            return redirect('add_variants')

    return render(request, 'add_storage.html')


 ######################### COLOR  #########################    

def screensize(request):
    screensizes = Screensize.objects.all()
    context = {
        'screensizes': screensizes
    }

    return render(request,'screensize.html', context)

def add_screensize(request):
    if request.method == 'POST':
        screensize = request.POST.get('screensize')
        if screensize:
            screensize = Screensize(screensize=screensize)
            screensize.save()
            return redirect('screensize') 
    return render(request, 'add_screensize.html')





 ######################### SEARCH  #########################    

def search(request):
    query = request.GET.get('q')

    print(query)
    
    
    if query:
        results = Account.objects.filter(username__icontains=query)
        print(results)
    
    else:
        results = []
    context = {
        "users": results,
        "query": query,
    }
    return render(request, 'user.html', context)


 ######################### ORDERS  ######################### 

def admin_orders(request):
    admin_orders = Order.objects.prefetch_related('orderitem_set').all().order_by('id')
    context = {
        'admin_orders':admin_orders
    }
    return render(request,'admin_order.html', context)

def update_orders(request,id):
    if request.method == 'POST':
        
        status = request.POST['status']

        order = Order.objects.get(id = id)

        order.status = status
        order.save()
        return redirect('admin_orders')
    
 ######################### Category Offers  ######################### 


def add_category_offer(request):
    if request.method == "POST":
        category_offer_name = request.POST.get("category_offer_name")
        category_offer_percentage = request.POST.get("category_offer_percentage")
        category_id = request.POST.get("category_name")
        
        category = Category.objects.get(category_name=category_id)
        
        category_offer = Categoryoffers.objects.create(
            category_offer_name = category_offer_name,
            category_offer_percentage = category_offer_percentage,
            category_name = category
        )

        return redirect('category')
 
    
 ######################### Product Offers  ######################### 


def add_product_offer(request):
    if request.method == "POST":
        product_offer_name = request.POST.get("product_offer_name")
        product_offer_percentage = request.POST.get("product_offer_percentage")
        product_id = request.POST.get("Product_name")
        
        product = Product.objects.get(Product_name=product_id)
        
        product_offer = Productoffers.objects.create(
            product_offer_name = product_offer_name,
            product_offer_percentage = product_offer_percentage,
            product_name = product
        )

        return redirect('product')


def add_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")
        discount_price = request.POST.get("discount_price")
        minimum_amount = request.POST.get("minimum_amount")
        
       
        
        coupon = Coupon.objects.create(
            coupon_code = coupon_code,
            discount_price = discount_price,
            minimum_amount = minimum_amount,
            
        )

        return redirect('coupon')


def coupon(request):
    coupons = Coupon.objects.all().order_by('uid')
    context = {
        'coupons': coupons
    }

    return render(request,'coupon.html', context)

def coupon_expired(request, coupon_id):
    coupon = Coupon.objects.get(uid=coupon_id)
    coupon.is_expired = True
    coupon.save()
    
    return redirect('coupon')

def coupon_list(request, coupon_id):
    coupon = Coupon.objects.get(uid=coupon_id)
    coupon.is_expired = False
    coupon.save()
    
    return redirect('coupon')

def update_refund_status(request, order_id):
    if request.method == 'POST':
        print('update_refund_status')
        print(order_id)
        order_product = Orderitem.objects.get(order_id = order_id)
        order_product.refund_status = 'refunded'
        order_product.save()


            # Add the refunded amount to the user's wallet
        print(order_product.order.user,'herererer')
        user_wallet, _ = Wallet.objects.get_or_create(user=order_product.order.user)
        user_wallet.balance +=  Decimal(str(order_product.price * order_product.order_quantity))
        user_wallet.save()

        return redirect('admin_orders')  # Redirect to a success page or appropriate URL

    return redirect('admin_orders')