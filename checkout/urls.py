from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from checkout.views import razorpaycheck




urlpatterns = [
    # path('',views.cart, name="cart"),
    path('',  views.checkout,name = 'checkout'),
    path('placeorder/',  views.placeorder,name = 'placeorder'),
    path('add_address/',views.add_address, name ='add_address'),

    path('proceed_to_pay/', razorpaycheck, name='proceed_to_pay'),
    
    path('orders/', views.orders, name='orders'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    path('invoice/',views.invoice, name = "invoice"),

    # path('my-order/', views.myorder),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

