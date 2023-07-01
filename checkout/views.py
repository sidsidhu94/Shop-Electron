from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import *
from products.models import *
from userprofile.models import *
from .models import Address, Order, Orderitem
from django.conf import settings
from django.http import JsonResponse

import razorpay
import random


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
        cart.cart_items.first()
    
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

    return render(request, 'checkout')


# def placeorder(request):
#     if request.method == "POST":
#         neworder = Order()
#         neworder.user = request.user
#         neworder.name = request.user.username

#         address_id = request.POST.get('selection')
#         neworder.address = Address.objects.get(id=address_id)
#         neworder.payment_mode = request.POST.get('payment_mode')

#         cart = Cart.objects.get(user=request.user)
#         total_price = cart.cart_total
#         neworder.total_price = total_price
#         payment_method = request.POST.get('payment_mode')

#         if payment_method == 'cod':
#             neworder.payment_mode = 'COD'
#         else:
#             try:
#                 client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
#                 payment = client.order.create(
#                     amount=int(total_price) * 100,
#                     currency='INR',
#                     payment_capture=1
#                 )
#                 order_item = {
#                     'cart': cart,
#                     'payment': payment,
#                     'amount': payment['amount']
#                 }
#             except Exception as e:
#                 print("Razorpay payment creation failed:", str(e))
#                 # Handle the error and return an appropriate response

#         trackno = "shop@electron" + str(random.randint(111111, 999999))
#         while Order.objects.filter(tracking_no=trackno).exists():
#             trackno = "shop@electron" + str(random.randint(111111, 999999))

#         neworder.tracking_no = trackno
#         neworder.save()

#         cart_items = Cartitems.objects.filter(cart=cart)
#         for item in cart_items:
#             variant = item.variant
#             variant.quantity -= int(item.variant_quantity)
#             variant.save()

#             order_item = Orderitem.objects.create(
#                 order=neworder,
#                 variant=item.variant,
#                 price=item.variant.price,
#                 order_quantity=item.variant_quantity,
#             )
#             order_item.save()

#         cart_items.delete()
#         messages.success(request, "Your order has been placed.")
#         return redirect('home')

#     return redirect('home')


def placeorder(request):
    if request.method == "POST":
        neworder = Order()

        neworder.user = request.user
        neworder.name = request.user.username

        address_id = request.POST.get('selection')
        neworder.address = Address.objects.get(id=address_id)
        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.get(user=request.user)
        total_price = cart.cart_total

        neworder.total_price = total_price
        neworder.total_price_in_paise = neworder.total_price * 100

        neworder.payment_method = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        trackno =   str(random.randint(111111, 999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno =  str(random.randint(111111, 999999))

        neworder.tracking_no = trackno
        neworder.save()

        cartitem = Cartitems.objects.filter(cart=cart)

        for item in cartitem:
            variant = item.variant
            variant.quantity -= int(item.variant_quantity)
            variant.save()

            orderitem = Orderitem.objects.create(
                order=neworder,
                variant=item.variant,
                price=item.variant.price,
                order_quantity=item.variant_quantity,
            )
            orderitem.save()

        cartitem.delete()
        messages.success(request, "Your order has been placed.")

        payMode = request.POST.get('payment_mode')
        if payMode == "Razorpay":
            return JsonResponse({'status': 'Your order has been placed successfully'})

    return redirect('home')



@login_required
def razorpaycheck(request):
    cart = Cart.objects.get(user=request.user)
    total_price = cart.cart_total

    return JsonResponse({
        'total_price' : total_price
    })

def orders(request):
    orders = Order.objects.all()  # Fetch all orders from the database
    context = {'orders': orders}
    return render(request, 'orders.html', context)





# def placezzorder(request): this is right 
#     if request.method == "POST":
        
#         neworder = Order()

#         neworder.user = request.user  # Assign the user instance directly
#         neworder.name = request.user.username  # Set the name field to the username


#         # user = request.user
      
        
#         # neworder.name = user.username
        
#         print(neworder.user,"###################### hihi")


        

        
#         address_id = request.POST.get('selection')
#         neworder.address = Address.objects.get(id=address_id)
#         neworder.payment_mode = request.POST.get('payment_mode')

#         print(address_id,"####### ivide ethi #######")


#         cart = Cart.objects.get(user=request.user)
#         print(cart, "###########################################################################################3")
#         total_price = cart.cart_total
#         print(total_price ,"######################################################paisa illeh??")

#         neworder.total_price = total_price
#         print(neworder.total_price ,"######################################################rinasinde thalukal??")
#         payment_method = request.POST.get('payment_mode')
#         print('payment method:')
#         print(payment_method)

#         if payment_method == 'cod':
#             neworder.payment_mode = 'COD'
#         else:
#             client = razorpay.Client(auth = ("rzp_test_Uariryi2s2u5dv" , "rkS3FvZypoawRTL4FGnsGILi"))

           
#             payment = client.order.create({
#                 'amount' : int(total_price)* 100,
#                 'currency' : 'INR',
#                 'payment_capture' : 1,
#                 })
#             print( payment,"####################################################  ayitundeee")
#             neworder.payment_mode = payment['id']

#             print(neworder.payment_mode,"####################################################  ayitundeee")
#             order_data = {
#                 'cart' : cart,
#                 'payment': neworder.payment_mode,
#                 'amount': neworder.payment_mode['amount']

#             }

#         # neworder.payment_mode = 'COD'
        

#         trackno = "shop@electron" + str(random.randint(111111, 999999))
#         while Order.objects.filter(tracking_no=trackno).exists():
#             trackno = "shop@electron" + str(random.randint(111111, 999999))

#         neworder.tracking_no = trackno
#         neworder.save()
#         print(neworder,"....................###################### ivide")

        
#         cartitem = Cartitems.objects.filter(cart = cart)

#         for item in cartitem:
#             variant = item.variant
#             variant.quantity -= int(item.variant_quantity)
#             variant.save()
#             print(variant.quantity, "########################################################### njn ividund")

#             orderitem = Orderitem.objects.create(
#                 order=neworder,
#                 variant=item.variant,
#                 price=item.variant.price,
#                 order_quantity=item.variant_quantity,
#             )
#             orderitem.save()

            
        
#         cartitem.delete()
#         messages.success(request, "Your order has been placed.")
#         return redirect('home')

#     return redirect('home')



# def placeorder(request):
#     if request.method == "POST":
#         neworder = Order()
#         neworder.user = request.user
#         neworder.address = request.POST.get(address = request.address)
#         neworder.payment_mode = request.POST.get('payment_mode')

#         print(neworder.address,"############################")


#         cart = Cart.objects.filter(user = request.user)
#         total_price = 0
#         for item in cart:
#             total_price = sum(item.variant.price * item.variant_quantity)

#         neworder.total_price = total_price

#         trackno = "shop@electron"+str(random.randint(111111,999999))
#         while Order.objects.filter(traking_no = trackno) is None:
#             trackno = "shop@electron"+str(random.randint(111111,999999)) 
        
#         neworder.tracking_no = trackno

#         neworder.save()

#         neworderitems = Cart.objects.filter(user = request.user)
#         for item in neworderitems:
#             Orderitem.objects.create(
#                 order = neworder,
#                 variant = item.variant,
#                 price = item.variant.price,
#                 quantity = item.quantity,
#             )

#             orderproduct = Variant.objects.filter(id = item.variant.uid).first()
#             orderproduct.quantity = orderproduct.quantity - item.quantity
#             orderproduct.save()

#         Cart.objects.filter(user = request.user).delete()

#         messages.success(request,"Your order has been placed")



#     return redirect('home')

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

def invoice(request):
    return render(request,"invoice.html")