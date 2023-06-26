from django.shortcuts import render,redirect,get_object_or_404
from products.models import *
from .models import *
from registration.views import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.http import HttpResponse
import json
# Create your views here.

# def cart(request):

#     return render(request, 'cart.html')



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



# def add_to_cart(request, variant_id):
#     variant = Variant.objects.get(uid=variant_id)
#     user = request.user
#     cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    
#     # Check if the product already exists in the cart
#     cart_item, created = Cartitems.objects.get_or_create(
#         cart=cart,
#         variant=variant,
#     )
    
#     # Increase the quantity if the item already exists
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('cart')


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
                return JsonResponse({'message': 'Quantity updated successfully'})
            else:
                return JsonResponse({'message': 'Insufficient stock'})

        except Cartitems.DoesNotExist:
            return JsonResponse({'message': 'Cart item not found'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': 'Invalid request'})




# def update_quantity(request, variant_id):
#     if request.method == 'POST':
#         quantity = request.POST.get('quantity')

#         # Perform validation and update quantity in the database
#         try:
#             cart_item = Cartitems.objects.get(variant__uid=variant_id, cart__user=request.user)
            
#             # Check if quantity is within the available stock range
#             if int(quantity) <= cart_item.variant.stock:
#                 cart_item.variant_quantity = quantity
#                 cart_item.save()
#                 return JsonResponse({'message': 'Quantity updated successfully'})
#             else:
#                 return JsonResponse({'message': 'Insufficient stock'})

#         except Cartitems.DoesNotExist:
#             return JsonResponse({'message': 'Cart item not found'})
#         except Exception as e:
#             return JsonResponse({'message': str(e)})

#     return JsonResponse({'message': 'Invalid request'})





# def update_quantity(request, variant_id):
#     if request.method == 'POST':
#         quantity = request.POST.get('quantity')

#         # Perform validation and update quantity in the database
#         try:
#             cart_item = Cartitems.objects.get(variant__uid=variant_id, cart__user=request.user)
#             cart_item.variant_quantity = quantity
#             cart_item.save()
#             return JsonResponse({'message': 'Quantity updated successfully'})
#         except Cartitems.DoesNotExist:
#             return JsonResponse({'message': 'Cart item not found'})
#         except Exception as e:
#             return JsonResponse({'message': str(e)})

#     return JsonResponse({'message': 'Invalid request'})



# def add_to_cart(request, variant_id):
#     variant = Variant.objects.get(uid=variant_id)
#     print("############################", variant)
#     user = request.user
#     cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    
#     cart_items = Cartitems.objects.create(
#         cart=cart,
#         variant=variant,
#     )

#     cart_items.save()
#     print("#################",cart_items)
#     return redirect('cart')


def remove_cart(request,cart_item_uid):
    try:
        cart_item = Cartitems.objects.get(uid = cart_item_uid)
        cart_item.delete()
        print('##########################',cart_item.delete())
    except Exception as e:
        print(e)
    return redirect('cart')