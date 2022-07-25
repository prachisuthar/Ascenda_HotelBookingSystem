from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, CreateView, View
# from .forms import *
from django.urls import reverse_lazy
# from .forms import BookingForm, SignUpForm, LoginForm
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
