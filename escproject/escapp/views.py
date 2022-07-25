from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, CreateView, View
from .forms import *
from django.urls import reverse_lazy
from .forms import BookingForm, SignUpForm, LoginForm
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
import requests 
from pandas.io.json import json_normalize
import pandas as pd
import folium
from flask import request

# Create your views here.
def index(request):
    languages = Feature1.objects.all()
    return render(request,'index.html',{"languages":languages})


def f1(request):
    if request.method=='POST':
        country=request.POST['country']
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        guests_number=request.POST['guests_number']
        rooms_number=request.POST['rooms_number']

    #f1=Feature1.objects.create(country = country, start_date = start_date, end_date = end_date, guests_number = guests_number, rooms_number = rooms_number)
    Feature1.objects.filter(country = country).update(start_date = start_date, end_date = end_date, guests_number = guests_number, rooms_number = rooms_number)
    global Qcountry, Qstart_date, Qend_date, Qguests_number, Qrooms_number, Qdest_id
    def Qcountry():
        return country
    def Qstart_date():
        return start_date
    def Qend_date():
        return end_date
    def Qguests_number():
        return guests_number
    def Qrooms_number():
        return rooms_number
    #to obtain destination id 
    country_entry = Feature1.objects.filter(country = country).first()
    destination_id = country_entry.uid
    def Qdest_id():
        return destination_id

    return render(request,'index.html')

            
class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("escapp:index")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        user = User.objects.create_user(username, confirm_password, password)
        form.instance.user = user
        login(self.request, user)
       
        return super().form_valid(form) 

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('escapp:index')

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("escapp:index")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        
        if usr is not None and usr.customer:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Credentials"})

        return super().form_valid(form)


class BookLoginView(FormView):
    template_name = "booklogin.html"
    form_class = BookLoginForm
    success_url = reverse_lazy("escapp:booking")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        
        if usr is not None and usr.customer:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Credentials"})

        return super().form_valid(form)

class BookingView(CreateView):
    template_name = "booking.html"
    form_class = BookingForm
    success_url = reverse_lazy("escapp:index")   