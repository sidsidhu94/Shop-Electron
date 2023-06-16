from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from registration.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="required.Add a valid email address.")

    class Meta:
        model = Account
        fields = ('email','mobilenumber','username','password1','password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            registration = Account.objects.get(email=email)
        except Exception as e:
            return email
        
        raise forms.ValidationError("Email is already in use.")
        


    def clean_username(self):
        username  = self.cleaned_data['username']
        try:
            registration = Account.objects.get(username=username)
        except Exception as e:
            return username 
        
        raise forms.ValidationError("Username is already in use.")
        
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields =("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email= email, password=password):
                raise forms.ValidationError("invalid login")
                
        # def clean(self):
        # cleaned_data = super().clean()
        # email = cleaned_data.get('email')
        # password = cleaned_data.get('password')
        
        # if email and password:
        #     user = authenticate(email=email, password=password)
        #     if not user:
        #         raise ValidationError("Invalid login")