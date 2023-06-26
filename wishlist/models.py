from django.db import models
from django.contrib.auth.models import User
from products.models import Variant
from registration.models import *


# Create your models here.

class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.user.username} - {self.variant.name}'