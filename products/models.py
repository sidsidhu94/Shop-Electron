from django.db import models

# Create your models here.
from base.models import BaseModel
from django.utils.text import slugify
from PIL import Image


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
    price                       = models.IntegerField()
    quantity                    = models.IntegerField()
    is_listed                   = models.BooleanField(default=True)

    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        variant_name = f"{self.product} - {self.color} - {self.storage}"

        self.variant_name = variant_name
        super().save(*args, **kwargs)

    

    def __str__(self):
        return f"{self.product} - {self.color} - {self.storage}"