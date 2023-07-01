from django.db import models
from registration.models import Account
from products.models import Variant
from userprofile.models import *
from datetime import timedelta,datetime

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(Account , on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , null = False)

    address = models.ForeignKey(Address , on_delete= models.CASCADE ,null = False)
    total_price = models.FloatField(null = False)
    payment_mode=(
       
        ('Razorpay','Razorpay'),
        ('COD','COD'),
    )

    payment_mode = models.CharField(max_length=100, null = False)
    payment_id  = models.CharField(max_length=250, null = True)
    orderstatus = (
        ('pending','pending'),
        ('Out for Shipping','Out for Shipping'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),

    )
    status = models.CharField(max_length=150, choices= orderstatus,default="pending")
    message = models.TextField(null = True)
    tracking_no  = models.CharField(max_length=150, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # delivery_date = models.DateTimeField(default=datetime.now() + timedelta(days=7))

    # def save(self, *args, **kwargs):
    #     self.delivery_date = self.created_at + timedelta(days=7)
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return '{} - {}'.format(self.id ,self.tracking_no)
    

class Orderitem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    price = models.FloatField(null = False)
    order_quantity = models.IntegerField(null = False)

    # def __str__(self):
    #     return '{}-{}',format(self.order.id , self.order.tracking_no)