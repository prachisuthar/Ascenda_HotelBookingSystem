from dataclasses import fields
from distutils.sysconfig import customize_compiler
from tkinter.ttk import Widget
from django import forms
from .models import *
from .views import * 
from django.forms import ModelForm
from django.contrib.auth.models import User


# class DateInput(forms.DateInput):
#     input_type = 'date'


# class DestinationSearchForm(forms.ModelForm):
#     class Meta:
#         model = DestinationSearch
#         fields = ["country","pax","start_date", "end_date"]
#         widgets = {
#             'start_date' : DateInput(),
#             'end_date' : DateInput()
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get("start_date")
#         end_date = cleaned_data.get("end_date")
#         if end_date < start_date:
#             raise forms.ValidationError("End date should be greater than start date.")

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ["username", "password", "full_name", "password", "confirm_password"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
           raise forms.ValidationError("Username already exists. Please choose another username.")

        return uname 

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput()) 


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["first_name", "last_name", "phone_number","email", "request", "credit_card_no","billing_address", "cvv", "expiry"]


