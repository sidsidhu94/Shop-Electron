from django.contrib import admin
from django.conf import Settings
from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
  ##..........user side..........##
  path('',views.home, name= "home" ),
  path('register_view/', views.register_view, name="register_view"),
  path('login_view/', views.login_view, name="login_view"),
  path('logout_view/', views.logout_view, name="logout_view"),
  path('shop/',views.shop, name= "shop"),
  path('productdetails/<str:variant_id>/', views.productdetails, name='productdetails'),
  path('verify_otp/',verify_otp, name= "verify_otp"),
  


  

 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
