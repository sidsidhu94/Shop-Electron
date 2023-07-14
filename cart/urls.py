from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',views.cart, name="cart"),
    path('',  views.cart,name = 'cart'),
    # path('cart/add_to_cart/<str:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<str:variant_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_cart/<str:cart_item_uid>/',views.remove_cart, name ="remove_cart"),
    path('updateCartItemQuantity/',views.updateCartItemQuantity, name ="updateCartItemQuantity"),
    path('remove_coupon/<str:cart_id>/',views.remove_coupon, name ="remove_coupon"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

