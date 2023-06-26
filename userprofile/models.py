from django.db import models
from registration.models import Account

# Create your models here.

class Address(models.Model):
    user_id                     = models.ForeignKey(Account,on_delete=models.CASCADE, null=False)
    fullname                    = models.CharField(max_length=50, null = False, blank = False)  
    address                     = models.CharField(max_length=50, null = False, blank = False)
    district                    = models.CharField(max_length=50, null = False, blank = False)
    state                       = models.CharField(max_length=50, null = False, blank = False)
    pincode                     = models.BigIntegerField(null = False, blank = False)
    mobile                      = models.BigIntegerField(null = False, blank = False)
    
    