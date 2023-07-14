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
    def cart_items_total(self):
        cartitems = self.cart_items.all()
        total     = sum([item.cart_item_total for item in cartitems])

        return total

    @property
    def cart_total(self):
        total     = self.cart_items_total
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
    def cart_item_total(self):
        if self.variant.offer_price:
            return self.variant.offer_price * self.variant_quantity
      
        else:
            return self.variant.price * self.variant_quantity
    
    
    @property
    def get_total(self):
        if self.variant.offer_price:
            return self.variant.offer_price * self.variant_quantity
        else:
            return self.calculate_discounted_price()

    def calculate_discounted_price(self):
        category_offers = Categoryoffers.objects.filter(category_name=self.variant.product.category)
        product_offers = Productoffers.objects.filter(product_name=self.variant.product)
        combined_discount = 0

        if category_offers.exists() or product_offers.exists():
            for category_offer in category_offers:
                combined_discount += category_offer.category_offer_percentage
            for product_offer in product_offers:
                combined_discount += product_offer.product_offer_percentage

            discount_amount = self.variant.price * combined_discount / 100
            discounted_price = self.variant.price - discount_amount

            if discounted_price < 0:
                discounted_price = 0

            return discounted_price
        else:
            return self.variant.price

    

    