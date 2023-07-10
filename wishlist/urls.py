from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('wishlist/',views.wishlist,name="wishlist"),
    path('add_to_wishlist/<str:variant_id>/', views.add_to_wishlist, name="add_to_wishlist"),
    path('remove_wishlist/<str:variant_id>/',views.remove_wishlist, name ="remove_wishlist"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
