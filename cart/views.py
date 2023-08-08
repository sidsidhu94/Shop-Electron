from django.shortcuts import render,redirect,get_object_or_404
from products.models import *
from .models import *
from registration.views import *
from checkout.models import Order
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from django.db.models import Q

import json

def cart(request):
    user = request.user
    cart = Cart.objects.get(user = user,is_paid=False)
    print(user,"##################################################superuser.....")
    print(cart)
    if not cart:
        # Handle the case when no carts are found for the user.
        # For example, you might want to create a new cart for the user here.
        cart = Cart.objects.create(user=user)
        print(cart,'else block')
    else:
        cart = cart
        print(cart,"#333333333")

    cart_items = Cartitems.objects.filter(cart = cart)
    print(cart)
    subtotal = 0
    total = 0

    for cart_item in cart_items:
        subtotal += cart_item.variant.price * cart_item.variant_quantity
        
    total += subtotal

    context = {
        'cart' : cart,
        'cartitems': cart_items,
        'subtotal': subtotal,
        'total': total,
        }

    
    if request.method == "POST":
        coupon = request.POST.get('coupon')


        try:
            coupon_obj = Coupon.objects.get(coupon_code = coupon)
            coupon_used = Order.objects.filter(Q(user = user) & Q(coupon = coupon))
            print(coupon_used)
            
            print(coupon_obj,"################################################################################")

            if not coupon_obj:
                messages.warning(request,"Invalid Coupon")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if coupon_used :
                messages.warning(request, 'Coupon has already been used')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
            if cart.coupon:
                messages.warning(request, 'Coupon already applied.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

            if cart.cart_total < coupon_obj.minimum_amount:
                messages.warning(request, f'Amount should be greater than {coupon_obj.minimum_amount}.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if coupon_obj.is_expired:
                messages.warning(request, 'Coupon has expired.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            cart.coupon = coupon_obj
            cart.save()
            messages.success(request, 'Coupon Applied')
        
        except:
            coupon_obj = None



    return render(request, 'cart.html', context)


def add_to_cart(request, variant_id):
    
    
    
    if request.user.is_authenticated:
        variant = Variant.objects.get(uid=variant_id)
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
        print(cart,"######################################################3")
        
        # Retrieve all matching Cartitems objects
        cart_items = Cartitems.objects.filter(cart=cart, variant=variant)
        if cart_items.exists():
            # If multiple objects exist, update the quantity of the first object
            cart_item = cart_items.first()
            cart_item.variant_quantity += 1
            cart_item.save()
        else:
            # If no objects exist, create a new Cartitems object
            cart_item = Cartitems.objects.create(cart=cart, variant=variant, variant_quantity=1)
        print(cart_item,"##################################################################33")

        return redirect('shop')
    
    else:
        return redirect('login_view')
    


def updateCartItemQuantity(request):

    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        new_quantity = int(request.POST.get('new_quantity'))
        print(cart_item_id)
        print(new_quantity)
        try:
            cart_item = Cartitems.objects.get(uid=cart_item_id)
            if (cart_item.variant.quantity <= new_quantity) :
                print('error message')
                response= {
                    'success': False,'status': 'error', 'message': 'Not enough stock'
                    }
                return JsonResponse({'status': 'error', 'message': 'Not enough stock'})
            cart_item.variant_quantity = new_quantity

            cart_item.save()    
    
            # Get the updated cart item total and cart total
            cart_item_total = cart_item.cart_item_total
            cart = cart_item.cart
            sub_total = cart.cart_items_total
            cart_total = cart.cart_total
            print(cart_item_total,cart_total)

            # Update the response data
            
            return JsonResponse({
                'cart_item_total': cart_item_total,
                'sub_total' : sub_total,
                'cart_total': cart_total,
            })
        except Cartitems.DoesNotExist:
            response = {
                'error': 'Cart item not found.'
            }
            return JsonResponse(response, status=400)



def remove_cart(request,cart_item_uid):
    try:
        cart_item = Cartitems.objects.get(uid = cart_item_uid)
        cart_item.delete()
        print('##########################',cart_item.delete())
    except Exception as e:
        print(e)
    return redirect('cart')


def remove_coupon(request,cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon =  None 
    cart.save()
    messages.warning(request, 'Coupon Removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))