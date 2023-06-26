from django.urls import path
from . import views


urlpatterns = [
    path('profile/',views.profile, name = 'profile'),
    path('create_address/',views.create_address, name ='create_address'),
]
