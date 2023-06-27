from django.shortcuts import render,redirect
from .models import *
from cart.models import *
from django.contrib import messages


# Create your views here.
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
