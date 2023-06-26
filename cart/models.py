from django.db import models
from registration.models import Account
from products.models import *
from base.models import BaseModel

# Create your models here.

class Cart(BaseModel):
    user                = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="carts")
    is_paid             = models.BooleanField(default=True)

    @property
    def cart_total(self):
        cartitems = self.cart_items.all()
        total     = sum([item.get_total for item in cartitems])
        return total
    
    @property
    def get_cart_items(self):
        cartitems = self.cartitems_set.all()
        total     = sum([item.variant_quantity for item in cartitems])
        return total

class Cartitems(BaseModel):
    cart                = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    variant             = models.ForeignKey(Variant, on_delete=models.CASCADE, null = True,blank=True)
    variant_quantity    = models.IntegerField(default = 1)

    @property
    def get_total(self):
        return self.variant.price * self.variant_quantity
    

    # def get_total(self):
    #     return self.product.product_price * self.product_qty




        # def get_product_total(self):
    #     cart_items = self.cart_items.all()
    #     price = []

    #     for cart_items in cart_items:

        
    #         if cart_items.variant:
    #             variant_price = cart_items.variant
    #             price.append(variant_price)
    #     return sum(price)

    # def __str__(self):
    #     return str(self.uid)
    
    # def cart_total(self):
    #     cartitems =self.cartitems_set.all()
    #     total = sum(item.get_total for item in cartitems)
    #     return total

    # def get_cart_items(self):
    #     cartitems = self.cartitem_set.all()
    #     total     = sum([item.variant_quantity for item in cartitems])
    #     return total

   