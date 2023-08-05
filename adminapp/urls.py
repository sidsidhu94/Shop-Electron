from django.contrib import admin
from django.conf import Settings
from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


      ##..........admin side..........##
  path('admin/',views.admin_login, name="admin_login"),
  path('dashboard/',views.dashboard, name='dashboard'),
  path('admin_logout/',views.admin_logout, name ='admin_logout'),
  
  
      ##..........user side..........##
  path('user/',views.user,name='user'),
  path('block_user/<int:user_id>/',views.block_user,name='block_user'),
  path('unblock_user/<int:user_id>/',views.unblock_user, name='unblock_user'),
  
     ##..........product side..........## 
  path('product/',views.product, name='product'),
  path('add_products/',views.add_products, name = 'add_products'),
  path('list_product/<str:product_id>/', views.list_product, name='list_product'),
  path('unlist_product/<str:product_id>/', views.unlist_product, name='unlist_product'),
  path('update_product/<str:product_id>/', views.update_product, name='update_product'),

    ##..........category side..........## 
  path('category',views.category, name='category'),
  path('add_category/',views.add_category, name ='add_category'),
  path('delete_category/<str:category_id>/',views.delete_category,name = 'delete_category' ),
  path('update_category/<str:category_id>/', views.update_category, name='update_category'),
  path('list_category/<str:category_id>/', views.list_category, name='list_category'),
  path('unlist_category/<str:category_id>/', views.unlist_category, name='unlist_category'),

    ##..........variants side..........## 
  path('add_variants/',views.add_variants, name = 'add_variants'),
  path('variants/',views.variants, name = 'variants'),
  path('list_variants/<str:variants_id>/', views.list_variants, name='list_variants'),
  path('unlist_variants/<str:variants_id>/', views.unlist_variants, name='unlist_variants'), 
  path('update_variants/<str:variants_id>/', views.update_variants, name='update_variants'),
  
    ##..........color side..........##   
  path('add_color/',views.add_color, name ='add_color'),
  path('color/',views.color, name ='color'),
  
    ##..........storage side..........##    
  path('add_storage/',views.add_storage, name = 'add_storage'),
  path('storage/',views.storage, name = 'storage'),

    ##..........screensize side..........##    
  path('add_screensize/',views.add_screensize, name = 'add_screensize'),
  path('screensize/',views.screensize, name = 'screensize'),

    ##..........order side..........##   

  path('admin_orders/',views.admin_orders, name = 'admin_orders'),
  path('update_orders/<int:id>/',views.update_orders,name='update_orders'),

    ##..........search side..........##   
  path('search/',views.search,name='search'),

  ##..........offer side..........##   
  path('add_category_offer/',views.add_category_offer, name ='add_category_offer'),
  path('add_product_offer/',views.add_product_offer, name ='add_product_offer'),

  path('coupon/',views.coupon, name ='coupon'),
  path('add_coupon/',views.add_coupon, name ='add_coupon'),
  path('coupon_expired/<str:coupon_id>/', views.coupon_expired, name='coupon_expired'),
  path('coupon_list/<str:coupon_id>/', views.coupon_list, name='coupon_list'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
