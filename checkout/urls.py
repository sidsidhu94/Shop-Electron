from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',views.cart, name="cart"),
    path('',  views.checkout,name = 'checkout'),
    path('placeorder/',  views.placeorder,name = 'placeorder'),
    path('add_address/',views.add_address, name ='add_address'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

