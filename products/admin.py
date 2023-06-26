from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import *

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['category_name', 'slug', 'display_image']

#     def display_image(self, obj):
#         if obj.category_image:
#             return f'<img src="{obj.category_image.url}" alt="{obj.category_name}" width="10" height="10">'
#         else:
#             return 'No image'

#     display_image.allow_tags = True
#     display_image.short_description = 'Image'

admin.site.register(Category)


# class ProductImageAdmin(admin.StackedInline):
#     model =ProductImage

# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductImageAdmin]

admin.site.register(Product)

admin.site.register(VariantImage)

admin.site.register(Color)
admin.site.register(Storage)
admin.site.register(Variant)
admin.site.register(Brand)


