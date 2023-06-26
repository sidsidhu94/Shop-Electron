# def register(request):
#     if request.method =='POST':
#         form=Registration(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             phone_number = form.cleaned_data['phone_number']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             username = email.split("@")[0]
#             user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
#             user.phone_number = phone_number
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Please activate your account'
#             message = render_to_string('account/account_verification_email.html', {
#                 'user': user,
#                 'domain': current_site,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject, message, to=[to_email])
#             send_email.send()
#             # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            
#             messages.success(request,'Thank you for registering with us we had send you email for activation')
#             return redirect('/account/login/?command=verification&email='+email)

            
#     form=Registration()
#     context ={ 
#         'form':form,
#     }
#     return render(request,'account/register.html',context)
# def login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         user = auth.authenticate(email=email, password=password)
#         print(user)
#         if user is not None:
#             auth.login(request, user)
#             messages.success(request, 'You are now logged in.')
#             redirect
#         else:
#             messages.error(request, 'Invalid login credentials')
#             return redirect('login')
#     return render(request, 'account/login.html')
# def activate(request,uidb64,token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Congratulations! Your account is activated.')
#         return redirect('login')
#     else:
#         messages.error(request, 'Invalid activation link')
#         return redirect('register')