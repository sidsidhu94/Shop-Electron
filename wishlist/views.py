from django.shortcuts import render,redirect
from .models import *
from cart.models import *
from django.contrib import messages


# Create your views here.
# def wishlist(request):
#     user = request.user
#     wishlist = Wishlist.objects.filter(user=user).first()
#     wishlist_items = WishlistItem.objects.none()
    
#     if wishlist:
#         wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    
#     context = {
#         'wishlist_items': wishlist_items
#     }
    
#     return render(request, 'wishlist.html', context)


def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user = user).first()
    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist)
    print(wishlist,"################################")
    
    context = {
        'wishlist_item': wishlist_item
        
    }
    
    return render(request, 'wishlist.html',context)
 


def add_to_wishlist(request, variant_id):
    variant = Variant.objects.get(uid=variant_id)
    user = request.user
    wishlist, created = Wishlist.objects.get_or_create(user=user)

    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, variant=variant)

    if wishlist_item.exists():
        messages.info(request, 'This product already exists in your wishlist.')
    else:
        wishlist_item = WishlistItem.objects.create(wishlist=wishlist, variant=variant)

    return redirect('shop')


def remove_wishlist(request, variant_id):
    try:
        wishlist_item = WishlistItem.objects.filter(id=variant_id)

        wishlist_item.delete()

    except WishlistItem.DoesNotExist:
        pass

    return redirect('wishlist')


# def remove_wishlist(request, wishlist_item_uid):
#     try:
#         wishlist_item = WishlistItem.objects.get(uid=wishlist_item_uid)
#         wishlist_item.delete()
#         # print('##########################', wishlist_item.delete())
#     except Exception as e:
#         pass

#     return redirect('wishlist')