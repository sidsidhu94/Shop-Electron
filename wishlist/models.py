from django.db import models
from django.contrib.auth.models import User
from products.models import Variant
from registration.models import *
from base.models import BaseModel

# Create your models here.

class Wishlist(models.Model):
    user  = models.ForeignKey(Account ,  on_delete=models.CASCADE,related_name= "wishlist")




class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE,related_name="wishlist_items",blank= True, null = True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,null = True,blank=True)
   