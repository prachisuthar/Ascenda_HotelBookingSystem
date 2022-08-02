from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, CreateView, View
from .forms import *
from django.urls import reverse_lazy
from .forms import BookingForm, SignUpForm, LoginForm, BookLoginForm
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
import requests 
from pandas.io.json import json_normalize
import pandas as pd
import folium
from flask import request
from django.shortcuts import redirect
from django.core.paginator import Paginator
import re

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

    # return render(request,'hotellist.html')
    return redirect("http://127.0.0.1:8000/hotellist/")

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
            HotelList.objects.filter(hotel_id = hotel["id"]).update(hotelName=hotel['name'], address=hotel['address'], imageURL=(hotel['image_details']['prefix']+str(hotel['default_image_index'])+hotel['image_details']['suffix']))
        
        HotelList.objects.filter(hotelName="Not Available").delete()

        
        #for hotel in r_prices['hotels']:
            #HotelPricesF2.objects.create(hotel_id=hotel['id'], cheapest_price = hotel['lowest_price'])

        #hotels_set = HotelList.objects.all()
        #for hotel in hotels_set.iterator():
            #HotelList.objects.filter(hotel_id = hotel["id"]).update(cheapest_price = hotel['lowest_price'])

        #for hotel in r_prices['hotels']:
            #HotelList.objects.filter(hotel_id = hotel["id"]).update(cheapest_price = hotel['lowest_price'])

        all_hotels = HotelList.objects.all()
        paginator = Paginator(all_hotels, 5)
        page_number = self.request.GET.get('page')
        hotels_list = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
            

        context['hotels_list'] = hotels_list

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
            description = jsonAs_list[0]['description'], amenities_ratings = jsonAs_list[0]['amenities_ratings'],
            trustyou_score_overall = jsonAs_list[0]['trustyou.score.overall'], trustyou_score_solo = jsonAs_list[0]['trustyou.score.solo'],
            trustyou_score_family= jsonAs_list[0]['trustyou.score.family'], trustyou_score_business= jsonAs_list[0]['trustyou.score.business'],
            default_image_index = jsonAs_list[0]['default_image_index'], cloudflare_image_url = jsonAs_list[0]['image_details.prefix'],
            image_details_suffix = jsonAs_list[0]['image_details.suffix']) #, imageIndices = jsonAs_list[0]['hires_image_index']
        obj = Feature3_info.objects.first()
        obj_id = obj.hotel_id
        try:
            amenities_new = str(hotel_info['amenities'])
            chars_to_remove_amenities = [": ", "True", "{", "}", "'"]
            for char in chars_to_remove_amenities:
                amenities_new = amenities_new.replace(char,"")
            amenities_new = re.sub(r"(\w)([A-Z])", r"\1 \2", amenities_new)
            amenities_new = amenities_new.lower()
            amenities_new = amenities_new.replace("t vin room", "TV in room")
            amenities = amenities_new
        except:
            amenities = "currently not available on site"
        Feature3_info.objects.filter(hotel_id = obj_id).update(amenities = amenities)
        try:
            Feature3_info.objects.filter(hotel_id = obj_id).update(imageIndices = jsonAs_list[0]['hires_image_index'])
        except:
            Feature3_info.objects.filter(hotel_id = obj_id).update(imageIndices = "1")
        amenitiesRatings = obj.amenities_ratings
        chars_to_remove = ["[", "]","'name'",": '", "', 'score'", "{", "}"]
        for char in chars_to_remove:
            amenitiesRatings = amenitiesRatings.replace(char,"")
        if amenitiesRatings == "":
            amenitiesRatings = "None"
        Feature3_info.objects.filter(hotel_id = obj_id).update(amenities_ratings = amenitiesRatings)

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



            
class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("escapp:index")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")

        if User.objects.filter(username = username).exists():
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Username already exists. Please enter a new username."})
        elif password != confirm_password:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Password and Re-Enter Password do not match."})
        else:
            user = User.objects.create_user(username, confirm_password, password)
            form.instance.user = user
            login(self.request, user)

            return super().form_valid(form) 

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
    success_url = reverse_lazy("escapp:accountinfo")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        
        if usr is not None and usr.customer:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Credentials"})

        return super().form_valid(form)


class DeleteUserView(FormView):
    template_name = "deleteuser.html"
    form_class = LoginForm
    success_url = reverse_lazy("escapp:confirmdelete")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        
        if usr is not None and usr.customer:
            User.objects.filter(username=uname).delete()
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Credentials"})

        return super().form_valid(form)

class BookingView(CreateView):
    template_name = "booking.html"
    form_class = BookingForm
    success_url = reverse_lazy("escapp:index") 


class StartBooking(CreateView):
    template_name = "booking.html"
    form_class = BookingForm
    success_url = reverse_lazy("escapp:confirmtransaction") 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        room = HotelRoomsInfo.objects.get(slug = url_slug)
        context["room"] = room
        booking_key = room.booking_key
        global bookingKey_forUse
        def bookingKey_forUse():
            return booking_key

    # def store_key(request):
    #     if request.method=='POST':
    #         key = request.POST[bookingKey_forUse]

    #     return key

        
        #global hlatitude
        #def hlatitude():
            #return hotel_latitude
            # bookingkey = bookingKey_forUse()

        
        return context

    def form_valid(self,form):
        cvv = form.cleaned_data.get("cvv")
        credit_card_no = form.cleaned_data.get("credit_card_no")
        expiry = form.cleaned_data.get("expiry")


        if len(str(cvv)) != 3:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "CVV can only be 3 digits. Please re-enter your CVV"})

        if len(str(credit_card_no)) != 16:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Credit Card Number can only be 16 digits. Please re-enter your Credit Card Number"})

        if len(str(expiry)) != 4:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Credit Card Expiry Date can only be 4 digits. Please re-enter it in the format of MMYY"})

        return super().form_valid(form)


class ConfirmTransactionView(TemplateView):
    template_name = "confirmtransaction.html"

    def get_context_data(self, **kwargs):

        form_obj = Booking.objects.last()
        cvv_of_obj = form_obj.cvv
        Booking.objects.filter(cvv = cvv_of_obj).update(booking_key = bookingKey_forUse())

        return super().get_context_data(**kwargs)

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html" 

class AccountinfoView(TemplateView):
    template_name = "accountinfo.html" 

class CheckDeleteAccountView(TemplateView):
    template_name = "checkdeleteaccount.html"

class ConfirmDeleteView(TemplateView):
    template_name = "confirmdelete.html"

    def del_user(request, username):    

        u = User.objects.get(username = username)
        u.delete()

        return render(request, 'confirmdelete.html')     

class HotelPictures(TemplateView):
    template_name = "hotelpictures.html"

    def get_context_data(self, **kwargs):
        HotelPicturesModel.objects.all().delete()
        #each time u call the query u must clear the database!!! so that u dont see extra stuff
        hotel_obj = Feature3_info.objects.first()
        imageIndices_arr = (hotel_obj.imageIndices).split(",")
        for element in imageIndices_arr:
            HotelPicturesModel.objects.create(imageURL = hotel_obj.cloudflare_image_url + str(element) + hotel_obj.image_details_suffix)
                
        context = super().get_context_data(**kwargs)
        context['hotel_pictures'] = HotelPicturesModel.objects.all()

        return context



class BookingDoneView(TemplateView):
    template_name = "bookingdone.html"


class BookingHistoryView(TemplateView):
    template_name = "bookinghistory.html"