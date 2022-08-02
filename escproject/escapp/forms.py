from django import forms
from .models import *
from .views import * 
from django.forms import ModelForm
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Customer
        fields = ["username", "password", "full_name", "password", "confirm_password", "email"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
           raise forms.ValidationError("Username already exists. Please choose another username.")

        return uname 
    

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput()) 


class BookLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput()) 

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["first_name", "last_name", "phone_number","email", "request", "bank", "credit_card_no","billing_address", "cvv", "expiry"]

