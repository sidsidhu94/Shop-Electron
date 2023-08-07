from django.shortcuts import render,redirect
from registration.models import *
from .models import *
from django.shortcuts import render, redirect
from .models import Address
# Create your views here.


# def profile(request):

#     return render(request, 'profile.html')


def profile(request):
    user_id = request.user.id
    addresses = Address.objects.filter(user_id=user_id)
    wallet = Wallet.objects.get(user_id = user_id)
   
    context = {
        'addresses': addresses,
        'wallet' :wallet,
    }
    return render(request, 'profile.html', context)



def create_address(request):
    if request.method == 'POST':
        user_id = request.user  
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        mobile = request.POST.get('mobile')
        
        address = Address(
                          user_id=user_id, 
                          fullname=fullname, 
                          address=address,
                          district=district, 
                          state=state, 
                          pincode=pincode, 
                          mobile=mobile
                          )
        address.save()
        
        return redirect('checkout')  
    
    return render(request, 'add_address.html')

def delete_address2(request,id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('checkout') 

