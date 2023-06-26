# from django.shortcuts import render
# from .models import *
# # Create your views here.


# def productdetails(request, variant_id):
#     try :
#         variant = Variant.objects.get(uid  = variant_id)
#         context ={
#             'variant' : variant
#          }
#         return render(request ,"productdetails.html", context )
    
#     except Exception as e:
#         print(e) 