from django.shortcuts import render,redirect,get_object_or_404
from products.models import *
from .models import *
from registration.views import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import json

def cart(request):
    user = request.user
    cart = Cart.objects.get(user = user)
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
            print(coupon_obj,"################################################################################")

            if not coupon_obj:
                messages.warning(request,"Invalid Coupon")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if coupon_obj.:
                messages.warning(request, 'Coupon has been applied.')
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
    variant = Variant.objects.get(uid=variant_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    
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

    return redirect('cart')


# def cart(request):
#     user = request.user
#     cart = Cart.objects.get(user = user)
#     cart_items = Cartitems.objects.filter(cart = cart)
#     print(cart)
#     subtotal = 0
#     total = 0
    
#     for cart_item in cart_items:
#         subtotal += cart_item.variant.price * cart_item.variant_quantity
        
#     total += subtotal

#     context = {
#         'cart' : cart,
#         'cartitems': cart_items,
#         'subtotal': subtotal,
#         'total': total,
#     }

#     return render(request, 'cart.html', context)


# from django.http import JsonResponse
# from django.shortcuts import redirect

# def add_to_cart(request, variant_id):
#     variant = Variant.objects.get(uid=variant_id)
#     user = request.user
#     cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    
#     # Retrieve all matching Cartitems objects
#     cart_items = Cartitems.objects.filter(cart=cart, variant=variant)
    
#     if cart_items.exists():
#         # If multiple objects exist, update the quantity of the first object
#         cart_item = cart_items.first()
#         cart_item.variant_quantity += 1
#         cart_item.save()
#     else:
#         # If no objects exist, create a new Cartitems object
#         cart_item = Cartitems.objects.create(cart=cart, variant=variant, variant_quantity=1)

#     # Display SweetAlert message
#     message = f"Item {variant.variant_name} added to cart!"
#     messages.success(request, message)
    
#     return JsonResponse({'success': True})

#     message = f"Item {variant.variant_name} added to cart!"
#     response_data = {'message': message}
#     return JsonResponse(response_data)




# def add_to_cart(request, variant_id):
#     variant = Variant.objects.get(uid=variant_id)
#     user = request.user
#     cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    
#     # Retrieve all matching Cartitems objects
#     cart_items = Cartitems.objects.filter(cart=cart, variant=variant)
    
#     if cart_items.exists():
#         # If multiple objects exist, update the quantity of the first object
#         cart_item = cart_items.first()
#         cart_item.variant_quantity += 1
#         cart_item.save()
#     else:
#         # If no objects exist, create a new Cartitems object
#         cart_item = Cartitems.objects.create(cart=cart, variant=variant, variant_quantity=1)

#     return redirect('cart')



######################################required

def update_quantity(request, variant_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')

        # Perform validation and update quantity in the database
        try:
            cart_item = Cartitems.objects.get(variant__uid=variant_id, cart__user=request.user)
            
            # Check if quantity is within the available stock range
            if int(quantity) <= cart_item.variant.stock:
                cart_item.variant_quantity = quantity
                cart_item.save()
                
                # Recalculate the subtotal and total in the cart
                cart = Cart.objects.get(user=request.user)
                cart_items = Cartitems.objects.filter(cart=cart)
                subtotal = 0
                total = 0
                
                for item in cart_items:
                    subtotal += item.variant.price * item.variant_quantity
                
                total += subtotal
                
                # Update the cart's subtotal and total
                cart.subtotal = subtotal
                cart.total = total
                cart.save()
                
                return JsonResponse({'message': 'Quantity updated successfully'})
            else:
                return JsonResponse({'message': 'Insufficient stock'})

        except Cartitems.DoesNotExist:
            return JsonResponse({'message': 'Cart item not found'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': 'Invalid request'})





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