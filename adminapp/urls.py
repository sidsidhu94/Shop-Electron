from django.contrib import admin
from django.conf import Settings
from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


      ##..........admin side..........##
  path('',views.admin_login, name="admin_login"),
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

  
    ##..........color side..........##   
  path('add_color/',views.add_color, name ='add_color'),
  path('color/',views.color, name ='color'),
  
    ##..........storage side..........##    
  path('add_storage/',views.add_storage, name = 'add_storage'),
  path('storage/',views.storage, name = 'storage'),

    ##..........search side..........##   
  path('search/',views.search,name='search'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
