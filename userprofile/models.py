from django.db import models
from registration.models import Account

# Create your models here.

class Address(models.Model):
    user_id                     = models.ForeignKey(Account,on_delete=models.CASCADE, null=False)
    fullname                    = models.CharField(max_length=50, null = False, blank = False)  
    address                     = models.CharField(max_length=50, null = False, blank = False)
    district                    = models.CharField(max_length=50, null = False, blank = False)
    state                       = models.CharField(max_length=50, null = False, blank = False)
    # country                     = models.CharField(max_length=50, null = False, blank = False)
    pincode                     = models.BigIntegerField(null = False, blank = False)
    mobile                      = models.BigIntegerField(null = False, blank = False)
    

class Wallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=False)

    def _str_(self):
        return f"Wallet of {self.user.username}"

    def save(self, *args, **kwargs):
        if self.balance  >1:
            self.is_available = True
        else:
            self.is_available = False
        super().save(*args, **kwargs)