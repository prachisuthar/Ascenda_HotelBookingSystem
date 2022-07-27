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

class HotelListView(TemplateView):
    template_name = "hotellist.html"

    def get_context_data(self, **kwargs):
        HotelList.objects.all().delete()
        #each time u call the query u must clear the database!!! so that u dont see extra stuff

        #query = {'destination_id':'WD0M', 'checkin':'2022-09-18', 'checkout':'2022-09-19', 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests':'2', 'partner_id':'1'}
        rooms = Qrooms_number()
        query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number(), 'partner_id':'1'}
        
        if (rooms == 2):
            query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number()|Qguests_number(), 'partner_id':'1'}
        elif (rooms == 3):
            query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number()|Qguests_number()|Qguests_number(), 'partner_id':'1'} 
        elif (rooms == 4):
            query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number()|Qguests_number()|Qguests_number()|Qguests_number(), 'partner_id':'1'}
        elif (rooms == 5):
            query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number()|Qguests_number()|Qguests_number()|Qguests_number()|Qguests_number(), 'partner_id':'1'}
        for i in range(3):
            response_prices = requests.get('https://hotelapi.loyalty.dev/api/hotels/prices?', params=query)
        r_prices = response_prices.json()
        for hotel in r_prices['hotels']:
            HotelList.objects.create(hotel_id=hotel['id'], cheapest_price=hotel['lowest_price'])
        for i in range(3):
            response_nonprices = requests.get('https://hotelapi.loyalty.dev/api/hotels?', params=query)
        r_nonprices = response_nonprices.json()
        for hotel in r_nonprices:
            HotelList.objects.filter(hotel_id = hotel["id"]).update(hotelName=hotel['name'], address=hotel['address'])
        
        HotelList.objects.filter(hotelName="Not Available").delete()

        
        #for hotel in r_prices['hotels']:
            #HotelPricesF2.objects.create(hotel_id=hotel['id'], cheapest_price = hotel['lowest_price'])

        #hotels_set = HotelList.objects.all()
        #for hotel in hotels_set.iterator():
            #HotelList.objects.filter(hotel_id = hotel["id"]).update(cheapest_price = hotel['lowest_price'])

        #for hotel in r_prices['hotels']:
            #HotelList.objects.filter(hotel_id = hotel["id"]).update(cheapest_price = hotel['lowest_price'])


        context = super().get_context_data(**kwargs)
        # context['country_list'] = DestinationSearch.country.

        context['hotels_list'] = HotelList.objects.all()

        return context

class HotelInfoView(TemplateView):
    template_name = "hotelinfo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        hotel = HotelList.objects.get(slug = url_slug)
        #context["hotel"] = hotel
        
        hotelID = hotel.hotel_id
        global hotel_ID
        def hotel_ID():
            return hotelID
        #call hotel info API
        api_link = "https://hotelapi.loyalty.dev/api/hotels/"
        new_api_link = api_link + hotelID
        for i in range(4):
            response = requests.get(new_api_link)
        hotel_info = response.json()
        Feature3_info.objects.all().delete()
        hotel_infoDF0 = pd.json_normalize(hotel_info) #,  record_path = "amenities_ratings"
        json_hotel_info = hotel_infoDF0.to_json(orient="records")
        jsonAs_list = json.loads(json_hotel_info)

        Feature3_info.objects.create(hotel_id = jsonAs_list[0]['id'], hotel_name = jsonAs_list[0]['name'], hotel_address = jsonAs_list[0]['address'],
            latitude = jsonAs_list[0]['latitude'], longitude = jsonAs_list[0]['longitude'], rating = jsonAs_list[0]['rating'],
            amenities_ratings = jsonAs_list[0]['amenities_ratings'], description = jsonAs_list[0]['description'], 
            trustyou_score_overall = jsonAs_list[0]['trustyou.score.overall'], trustyou_score_solo = jsonAs_list[0]['trustyou.score.solo'],
            trustyou_score_family= jsonAs_list[0]['trustyou.score.family'], trustyou_score_business= jsonAs_list[0]['trustyou.score.business'],
            default_image_index = jsonAs_list[0]['default_image_index'], cloudflare_image_url = jsonAs_list[0]['image_details.prefix'],
            image_details_suffix = jsonAs_list[0]['image_details.suffix'])
        obj = Feature3_info.objects.first()
        hotel_latitude = jsonAs_list[0]['latitude']
        hotel_longitude = jsonAs_list[0]['longitude']

        global hlatitude
        def hlatitude():
            return hotel_latitude
        global hlongitude
        def hlongitude():
            return hotel_longitude
        Feature3_info.objects.filter(hotel_id = hotelID).update(image_url_ForUse = Feature3_info.objects.first().cloudflare_image_url + Feature3_info.objects.first().default_image_index + Feature3_info.objects.first().image_details_suffix)
        hotel1 = Feature3_info.objects.first()

        context["hotel1"] = hotel1

        # context['country_list'] = DestinationSearch.country.

        #context = { "hotel_name": hotel.hotelName, "cheapest_price": hotel.cheapest_price, "address": hotel.address, "hotel_id":hotel.hotel_id}

        return context

class HotelRoomsView(TemplateView):
    template_name = "hotelrooms.html"

    def get_context_data(self, **kwargs):
        HotelRoomsInfo.objects.all().delete()
        #each time u call the query u must clear the database!!! so that u dont see extra stuff
        
        rooms = Qrooms_number()
        query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number(), 'partner_id':'1'}
        
        if (rooms == 2):
            query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number()|Qguests_number(), 'partner_id':'1'}
        elif (rooms == 3):
            query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number()|Qguests_number()|Qguests_number(), 'partner_id':'1'} 
        elif (rooms == 4):
            query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number()|Qguests_number()|Qguests_number()|Qguests_number(), 'partner_id':'1'}
        elif (rooms == 5):
            query = {'destination_id': Qdest_id(), 'checkin': Qstart_date(), 'checkout': Qend_date(), 'lang':'en_US', 'country_code': 'SG', 'currency':'SGD', 'guests': Qguests_number()|Qguests_number()|Qguests_number()|Qguests_number()|Qguests_number(), 'partner_id':'1'}
        
        api_link1 = "https://hotelapi.loyalty.dev/api/hotels/"
        api_link3 = "/price?"
        api_link2 = hotel_ID()
        api_link_rooms = api_link1 + api_link2 + api_link3
        for i in range(3):
            response = requests.get(api_link_rooms, params=query)

        roomsData = response.json()
        roomsData_json = roomsData['rooms']
        #flatten json data
        hotel_rooms_DF = pd.json_normalize(roomsData_json) 
        json_rooms_info = hotel_rooms_DF.to_json(orient="records")
        final_rooms_data = json.loads(json_rooms_info)

        for hotelRoom in final_rooms_data:
            HotelRoomsInfo.objects.create(booking_key = hotelRoom['key'], roomNormalizedDescription = hotelRoom['roomNormalizedDescription'],
                free_cancellation = hotelRoom['free_cancellation'], price = hotelRoom['price'],
                long_description = hotelRoom['long_description'], amenities = ', '.join(hotelRoom['amenities']),
                price_type = hotelRoom['price_type'], max_cash_payment = hotelRoom['max_cash_payment'], coverted_max_cash_payment = hotelRoom['coverted_max_cash_payment'], 
                points = hotelRoom['points'], bonuses = hotelRoom['bonuses'], lowest_price = hotelRoom['lowest_price'],
                converted_price = hotelRoom['converted_price'], lowest_converted_price = hotelRoom['lowest_converted_price'], 
                chargeableRate = hotelRoom['chargeableRate'], market_rates = hotelRoom['market_rates'], imageURL_forUse = hotelRoom['images'][0]['url']
                )
                
        
        context = super().get_context_data(**kwargs)

        context['hotel_rooms'] = HotelRoomsInfo.objects.all()

        return context

class ViewMap(TemplateView):
    template_name = "hotelInfo_map.html"


    def get_context_data(self, **kwargs):
        
        latitude = hlatitude()
        longitude = hlongitude()

        figure = folium.Figure()
        m = folium.Map(
            location=[latitude, longitude],
            tiles='CartoDB Positron',
            zoom_start=4,
        )
        m.add_to(figure)

        folium.Marker(
            location=[latitude, longitude],
            popup='Hotel Location',
            icon=folium.Icon(color='green')
        ).add_to(m)

        figure.render()
        return {"map": figure}

    def get(self, request, *args, **kwargs):
        latitude = request.session.get('latitude')
        longitude = request.session.get('longitude')

        return super().get(request, *args, **kwargs)

class StartBooking(TemplateView):
    template_name = "startbooking.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        room = HotelRoomsInfo.objects.get(slug = url_slug)
        context["room"] = room
        #room.booking_key
        #global hlatitude
        #def hlatitude():
            #return hotel_latitude

        
        return context

            
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

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html" 

class AccountinfoView(TemplateView):
    template_name = "accountinfo.html" 


