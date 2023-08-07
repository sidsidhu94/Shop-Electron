from django.contrib import admin
from django.conf import Settings
from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    
  ##..........user side..........##
  path('',views.home, name= "home" ),
  path('register_view/', views.register_view, name="register_view"),
  path('login_view/', views.login_view, name="login_view"),
  path('logout_view/', views.logout_view, name="logout_view"),
  # path('forgot_password/', views.forgot_password, name="forgot_password"),
  path('forgot_password/', forgot_password, name='forgot_password'),
  # path('reset_password/<str:token>/', views.reset_password, name='reset_password'),



  path('shop/',views.shop, name= "shop"),
  path('shop_by_category/<str:category_name>/', views.shop_by_category, name='shop_by_category'),
  path('shop_by_price', views.shop_by_price, name='shop_by_price'),
  path('productdetails/<str:variant_id>/', views.productdetails, name='productdetails'),
  path('verify_otp/',verify_otp, name= "verify_otp"),
  


  

 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
