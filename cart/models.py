from django.db import models
from registration.models import Account
from products.models import *
from base.models import BaseModel

# Create your models here.

class Cart(BaseModel):
    user                = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="carts")
    coupon              = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank= True)
    is_paid             = models.BooleanField(default=True)

    @property

    def cart_total(self):
        cartitems = self.cart_items.all()
        total     = sum([item.get_total for item in cartitems])

        if self.coupon:
            return total - self.coupon.discount_price

        return total
    
    @property
    def get_cart_items(self):
        cartitems = self.cart_items.all()
        total     = sum([item.variant_quantity for item in cartitems])
        return total

class Cartitems(BaseModel):
    cart                = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    variant             = models.ForeignKey(Variant, on_delete=models.CASCADE, null = True,blank=True)
    variant_quantity    = models.IntegerField(default = 1)

    @property
    def get_total(self):
        return self.variant.price * self.variant_quantity
    

    