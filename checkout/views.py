from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import *
from products.models import *
from userprofile.models import *


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
    if cart and cart.cart_items.exists() and cart.cart_items.first().variant.quantity < cart.cart_items.first().variant_quantity:
        # Handle the case where the variant quantity is less than the cart item quantity
        cart.cart_items.first().delete()
    
    cart_items = cart.cart_items.all()
    total_price = sum(item.variant.price * item.variant_quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, "checkout.html", context)




def add_address(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        mobile = request.POST.get('mobile')

        address_obj = Address(
            user_id=user_id,
            fullname=fullname,
            address=address,
            District=district,
            state=state,
            pincode=pincode,
            mobile=mobile
        )
        address_obj.save()

        return redirect('profile')  

    return render(request, 'checkout.html')



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