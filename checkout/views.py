from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import *
from products.models import *
from userprofile.models import *
from .models import Address, Order

# Create your views here.

# def checkout(request):
#     rawcart = Cart.objects.filter(user = request.user)
#     for item in rawcart:
#         if item.variant_quantity > item.Variant.variant_quantity:
#             Cart.objects.delete(uid = item.cart_item_uid)
    
#     cart_items = Cart.objects.filter(user = request.user)
#     total_price = 0
#     for item in cart_items:
#         total_price = total_price + item.variant.price * item.variant_quantity

#     context = {
#         'cart_items' : cart_items,
#         'total_price' :total_price,
#     }

#     return render(request,"checkout.html", context)

def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    addresses = Address.objects.filter(user_id = request.user)
    if cart and cart.cart_items.exists() and cart.cart_items.first().variant.quantity < cart.cart_items.first().variant_quantity:
        # Handle the case where the variant quantity is less than the cart item quantity
        cart.cart_items.first().delete()
    
    cart_items = cart.cart_items.all()
    total_price = sum(item.variant.price * item.variant_quantity for item in cart_items)

    
    return render(request, "checkout.html", locals())




def add_address(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  
        name = request.POST.get('name')
        address = request.POST.get('address')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        mobile = request.POST.get('mobile')

        address_obj = Address(
            user_id=user_id,
            name=name,
            address=address,
            District=district,
            state=state,
            pincode=pincode,
            mobile=mobile
        )
        address_obj.save()

        return redirect('profile')  

    return render(request, 'checkout.html')
 
 

def placeorder(request):
    if request.method == "POST":
        neworder = Order()
        neworder.user = request.user
        neworder.address = Address()
        neworder.payment_mode = request.POST.get()

        return redirect('checkout')

# def add_address(request):

#     return render(request ,'add_address.html')


# def address(request):
#     if request.method == "POST":
#         user_id              = request.user_id
#         firstname           = request.POST.get('firstname')
#         lastname            = request.POST.get('lastname')
#         housename           = request.POST.get('housename')
#         address              = request.POST.get('address')
#         district             = request.POST.get('district')
#         state                = request.POST.get('state')
#         pincode              = request.POST.get('pincode')
#         mobile               = request.POST.get('mobile')


#         address_obj = Address(
#             user_id=user_id,
#             first_name=firstname,
#             last_name=lastname,
#             house_name=housename,
#             address=address,
#             district=district,
#             state=state,
#             pincode=pincode,
#             mobile=mobile
#         )  

#         address_obj.save()

#         return render(request, 'checkout.html')