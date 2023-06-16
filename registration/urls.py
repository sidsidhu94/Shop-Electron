from django.contrib import admin
from django.conf import Settings
from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
  ##..........user side..........##
  path('',views.index, name= "index" ),
  path('register/', register_view, name="register"),
  path('login/', login_view, name="login_view"),
  path('logout/', logout_view, name="logout_view"),
  path('shop/',shop, name= "shop"),
  path('verify_otp/',verify_otp, name= "verify_otp"),

  

  ##..........admin side..........##
  path('admin_login/',views.admin_login, name="admin_login"),
  path('dashboard/',views.dashboard, name='dashboard'),
  path('user/',views.user,name='user'),
  path('block_user/<int:user_id>/',views.block_user,name='block_user'),
  path('unblock_user/<int:user_id>/',views.unblock_user, name='unblock_user'),
  path('product/',views.product, name='product'),
  path('category',views.category, name='category'),
  path('admin_logout/',views.admin_logout, name ='admin_logout'),
  path('add_category/',views.add_category, name ='add_category'),
  path('add_variants/',views.add_variants, name = 'add_variants'),
  path('add_color/',views.add_color, name ='add_color'),
  path('add_storage/',views.add_storage, name = 'add_storage'),
  path('add_products/',views.add_products, name = 'add_products'),
  path('color/',views.color, name ='color'),
  path('storage/',views.storage, name = 'storage'),
  path('variants/',views.variants, name = 'variants'),
  path('search/',views.search,name='search'),
  path('delete_category/<str:category_id>/',views.delete_category,name = 'delete_category' ),
  path('update_category/<str:category_id>/', views.update_category, name='update_category'),
  path('product/<int:product_id>/list/', list_product, name='list_product'),
  path('product/<int:product_id>/unlist/', unlist_product, name='unlist_product'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
