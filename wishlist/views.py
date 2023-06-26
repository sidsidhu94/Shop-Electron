from django.shortcuts import render,redirect
from .models import *

# Create your views here.
def wishlist(request):
    # user = request.user
    # wishlist_items = WishlistItem.objects.filter(user=user)
    
    # context = {
    #     'wishlist_items': wishlist_items
    # }
    
    return render(request, 'wishlist.html')
 


# def wishlist(request):
#     user = request.user
#     wishlist_items = WishlistItem.objects.filter(user=user)
    
#     # Handle adding a product to the wishlist
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         product = Product.objects.get(id=product_id)
        
#         # Check if the product is already in the wishlist
#         if not WishlistItem.objects.filter(user=user, product=product).exists():
#             wishlist_item = WishlistItem(user=user, product=product)
#             wishlist_item.save()
    
#     context = {
#         'wishlist_items': wishlist_items
#     }
    
#     return render(request, 'wishlist.html', context)

