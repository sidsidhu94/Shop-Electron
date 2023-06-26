from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',views.cart, name="cart"),
    path('cart/',  views.cart,name = 'cart'),
    path('add_to_cart/<str:variant_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_cart/<str:cart_item_uid>/',views.remove_cart, name ="remove_cart"),
    path('cart/update_quantity/<str:variant_id>/',views.update_quantity, name ="update_quantity"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

