from django.db import models

# Create your models here.
from base.models import BaseModel
from django.utils.text import slugify
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from registration.models import Account



class Category(BaseModel):
    category_name               = models.CharField(max_length=100)
    slug                        = models.SlugField(unique=True, null=True,blank=True)
    category_image              = models.ImageField(upload_to= "category")
    is_listed                   = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     # Resize and optimize the image
    #     if self.category_image:
    #         image = Image.open(self.category_image)
    #         image.thumbnail((800, 800))
    #         image.save(self.category_image.path, optimize=True, quality=90)

    #     # Generate the slug
    #     if not self.slug:
    #         self.slug = slugify(self.category_name)

    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
            
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.category_name)
    #     super().save(*args, **kwargs)


class Product(BaseModel):
    Product_name                = models.CharField(max_length=100)
    slug                        = models.SlugField(unique=True,null=True,blank=True)
    category                    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    prodct_description          = models.TextField()
    brand                       = models.ForeignKey('Brand',on_delete= models.SET_NULL,null=True)
    image                       = models.ImageField(upload_to="product",null=True,blank=True)
    is_listed                   = models.BooleanField(default=True)
    
    def __str__(self):
        return self.Product_name

class VariantImage(BaseModel):
    variant                     = models.ForeignKey('Variant',on_delete=models.CASCADE, related_name="variantimages")
    image                       = models.ImageField(upload_to="variant_images")

 
class Color(BaseModel):
    color_name                  = models.CharField(max_length=30)
    
    def __str__(self):
        return self.color_name

class Storage(BaseModel):
    memory                      = models.CharField(max_length=30)

    def __str__(self):
        return self.memory
    
class Screensize(models.Model):
    screensize                  = models.CharField(max_length=30)
    
    def __str__(self):
        return self.screensize



class Brand(BaseModel):
    brand_name                  =models.CharField(max_length=50)
    brand_logo                  =models.ImageField(upload_to= 'brand_logo' )  

    def __str__(self):
        return self.brand_name
    

class Variant(BaseModel):
    product                     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    variant_name                = models.CharField(max_length=100,blank=True)
    color                       = models.ForeignKey(Color, on_delete=models.CASCADE)
    storage                     = models.ForeignKey(Storage, on_delete=models.CASCADE)
    screensize                  = models.ForeignKey(Screensize, on_delete=models.CASCADE, null = True)

    price                       = models.IntegerField()
    quantity                    = models.IntegerField()
    is_listed                   = models.BooleanField(default=True)

    @property
    def discount(self):
        category_offers = Categoryoffers.objects.filter(category_name=self.product.category)
        product_offers = Productoffers.objects.filter(product_name=self.product)
        discount = 0

        if category_offers.exists() or product_offers.exists():
            for category_offer in category_offers:
                discount += category_offer.category_offer_percentage
            for product_offer in product_offers:
               discount += product_offer.product_offer_percentage

        return discount



    @property
    def offer_price(self):
        category_offers = Categoryoffers.objects.filter(category_name=self.product.category)
        product_offers = Productoffers.objects.filter(product_name=self.product)
        combined_discount = 0

        if category_offers.exists() or product_offers.exists():
            for category_offer in category_offers:
                combined_discount += category_offer.category_offer_percentage
            for product_offer in product_offers:
                combined_discount += product_offer.product_offer_percentage

            discount_amount = self.price * combined_discount / 100
            discounted_price = self.price - discount_amount

            if discounted_price < 0:
                discounted_price = 0

            return discounted_price
        else:
            return None



    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        variant_name = f"{self.product} - {self.color} - {self.storage}"

        self.variant_name = variant_name
        super().save(*args, **kwargs)

    

    def __str__(self):
        return f"{self.product} - {self.color} - {self.storage}"
    


class Categoryoffers(models.Model):
    category_offer_name = models.CharField(max_length=20)
    category_offer_percentage = models.IntegerField(validators=[MaxValueValidator(99)])
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)

    def clean(self):
        if self.category_offer_percentage <= 0 or self.category_offer_percentage >= 100:
            raise ValidationError("Percentage must be between 1 and 99.")
    
    def __str__(self):
        return self.category_offer_name
    
class Productoffers(models.Model):
    product_offer_name = models.CharField(max_length=20)
    product_offer_percentage = models.IntegerField(validators=[MaxValueValidator(99)])
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)

    def clean(self):
        if self.product_offer_percentage <= 0 or self.product_offer_percentage >= 100:
            raise ValidationError("Percentage must be between 1 and 99.")
    
    def __str__(self):
        return self.product_offer_name
    


class Coupon(BaseModel):
    
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    is_applied = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount =models.IntegerField(default=500)
    
    def __str__(self):
        return self.coupon_code

