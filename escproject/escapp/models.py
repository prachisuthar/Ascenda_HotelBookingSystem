from django.db import models
import json
from django.contrib.auth.models import User 
import uuid
from datetime import datetime
# from .forms import ModelForm 
# Create your models here.

class Feature1(models.Model):
    country = models.CharField(max_length=250, blank=True, default="-")
    uid = models.CharField(max_length=250, blank=True)
    guests_number = models.PositiveIntegerField(blank=True, default = 3)
    rooms_number = models.PositiveIntegerField(blank=True, default = 3)
    start_date = models.DateField(blank=True, default = "2020-10-10")
    end_date = models.DateField(blank=True, default = "2020-11-11")
   
    

# class DestinationSearch(models.Model):
#     country = models.CharField(max_length=250, blank=True)
#     pax = models.PositiveIntegerField(blank=True)
#     start_date = models.DateField(blank=True)
#     end_date = models.DateField(blank=True)
   

# json_file_path0 = "destinations.json"

# with open(json_file_path0, 'r', encoding="utf8") as j:
#     searchResults0 = json.loads(j.read())

# for searchResult0 in searchResults0['results']: 
#     Feature1.objects.create(country = searchResult0['term'], uid = searchResult0['uid'])


#for searchResult0 in searchResults0['results']: 
    #DestinationSearch.objects.create(country = searchResult0['term'], pax=1, start_date = "2000-10-11", end_date = "2000-11-12")

#json_file_path1 = "Singapore_Hotels.json"

#with open(json_file_path1, 'r', encoding="utf8") as j:
    #searchResults1 = json.loads(j.read())

#for searchResult1 in searchResults1['results']: 
    #DestinationSearch.objects.create(country = searchResult1['name'], pax=1, start_date = "2000-10-11", end_date = "2000-11-12")

#json_file_path2 = "KL_Hotels.json"

#with open(json_file_path2, 'r', encoding="utf8") as j:
    #searchResults2 = json.loads(j.read())

#for searchResult2 in searchResults2['results']: 
    #DestinationSearch.objects.create(country = searchResult2['name'], pax=1, start_date = "2000-10-11", end_date = "2000-11-12")



class SingaporeHotelList(models.Model):
    hotel_name = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to = "singapore", blank=True)
    rating = models.PositiveIntegerField(blank=True)
    price = models.PositiveIntegerField(blank=True)

#json_file_path = "Singapore_Hotels.json"

#with open(json_file_path, 'r', encoding="utf8") as j:
    #sgsearchResults = json.loads(j.read())

#for sgsearchResult in sgsearchResults['results']: 
    #SingaporeHotelList.objects.create(hotel_name = sgsearchResult['name'], address = sgsearchResult['address'], image=sgsearchResult['imgix_url'], rating = sgsearchResult['rating'], price = sgsearchResult['imageCount'])

class KLHotelList(models.Model):
    hotel_name = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to = "kl", blank=True)
    rating = models.PositiveIntegerField(blank=True)
    price = models.PositiveIntegerField(blank=True)

#json_file_path = "KL_Hotels.json"

#with open(json_file_path, 'r', encoding="utf8") as j:
    #klsearchResults = json.loads(j.read())

#for klsearchResult in klsearchResults['results']: 
    #KLHotelList.objects.create(hotel_name = klsearchResult['name'], address = klsearchResult['address'], image = klsearchResult['imgix_url'], rating = klsearchResult['rating'], price = klsearchResult['imageCount'])

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)

    def __str__(self):
        return self.full_name

class HotelList(models.Model):
    hotelName = models.CharField(max_length=250, blank=True, default="Not Available")
    slug = models.SlugField(unique = True, default=uuid.uuid1)
    address = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to = "feat2", blank=True)
    cheapest_price = models.PositiveIntegerField(blank=True, default=0)
    hotel_id = models.CharField(max_length=250, blank=True, default = "")

class Booking(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.PositiveIntegerField()
    email = models.EmailField()
    request = models.CharField(max_length=5000)
    credit_card_no = models.PositiveIntegerField()
    expiry = models.PositiveBigIntegerField()
    cvv = models.PositiveIntegerField()
    billing_address = models.CharField(max_length=500)

class HotelPricesF2(models.Model):
    hotel_id = models.CharField(max_length=250, blank = True)
    cheapest_price = models.DecimalField(blank=True,decimal_places=20,max_digits=50,default=0)


#check: do i still need the below database?
class hotelNameToID(models.Model):
    hotel_name = models.CharField(max_length=250, blank = True)
    hotel_id = models.CharField(max_length=250, blank = True)

#the below code for the model hotelNameToID is NOT needed anymore! Do NOT uncomment out
#json_file_path_SG = "Singapore_Hotels.json"

#with open(json_file_path_SG, 'r', encoding="utf8") as j:
    #sgsearchResults = json.loads(j.read())

#for sgsearchResult in sgsearchResults['results']: 
    #hotelNameToID.objects.create(hotel_name = sgsearchResult['name'], hotel_id = sgsearchResult['id'])

#json_file_path_KL = "KL_Hotels.json"

#with open(json_file_path_KL, 'r', encoding="utf8") as j:
    #klsearchResults = json.loads(j.read())

#for klsearchResult in klsearchResults['results']: 
    #hotelNameToID.objects.create(hotel_name = klsearchResult['name'], hotel_id = klsearchResult['id'])

class Feature3_info(models.Model):
    hotel_id = models.CharField(max_length=250, blank = True, default = "None", null=True)
    hotel_name = models.CharField(max_length=250, blank = True, default = "None", null=True)
    hotel_address = models.CharField(max_length=250, blank = True, default = "None", null=True)
    latitude = models.CharField(max_length=250, blank = True, default = "None", null=True)
    longitude = models.CharField(max_length=250, blank = True, default = "None", null=True)
    rating = models.CharField(max_length=250, blank = True, default = "None", null=True)
    amenities_ratings = models.CharField(max_length=250, blank = True, default = "None", null=True)
    description = models.CharField(max_length=250, blank = True, default = "None", null=True)
    trustyou_score_overall = models.CharField(max_length=250, blank = True, default = "None", null=True)
    trustyou_score_solo = models.CharField(max_length=250, blank = True, default = "None", null=True)
    trustyou_score_couple = models.CharField(max_length=250, blank = True, default = "None", null=True)
    trustyou_score_family = models.CharField(max_length=250, blank = True, default = "None", null=True)
    trustyou_score_business = models.CharField(max_length=250, blank = True, default = "None", null=True)
    image_details_suffix = models.CharField(max_length=250, blank = True, default = "None", null=True)
    default_image_index = models.CharField(max_length=250, blank = True, default = "None", null=True)
    cloudflare_image_url = models.CharField(max_length=250, blank = True, default = "None", null=True)
    image_url_ForUse = models.CharField(max_length=250, blank = True, default = "None", null=True)

class HotelRoomsInfo(models.Model):
    booking_key = models.CharField(max_length=250, blank = True, default = "None", null=True)
    roomDescription = models.CharField(max_length=250, blank = True, default = "None", null=True)
    roomNormalizedDescription = models.CharField(max_length=250, blank = True, default = "None", null=True)
    free_cancellation = models.CharField(max_length=250, blank = True, default = "None", null=True)
    roomAdditionalInfo = models.CharField(max_length=250, blank = True, default = "None", null=True)
    surcharges = models.CharField(max_length=250, blank = True, default = "None", null=True)
    long_description = models.CharField(max_length=250, blank = True, default = "None", null=True)
    images_URLs = models.CharField(max_length=250, blank = True, default = "None", null=True)
    amenities = models.CharField(max_length=250, blank = True, default = "None", null=True)
    price_type = models.CharField(max_length=250, blank = True, default = "None", null=True)
    max_cash_payment = models.CharField(max_length=250, blank = True, default = "None", null=True)
    coverted_max_cash_payment = models.CharField(max_length=250, blank = True, default = "None", null=True)
    points = models.CharField(max_length=250, blank = True, default = "None", null=True)
    bonuses = models.CharField(max_length=250, blank = True, default = "None", null=True)
    lowest_price = models.CharField(max_length=250, blank = True, default = "None", null=True)
    price = models.CharField(max_length=250, blank = True, default = "None", null=True)
    converted_price = models.CharField(max_length=250, blank = True, default = "None", null=True)
    lowest_converted_price = models.CharField(max_length=250, blank = True, default = "None", null=True)
    chargeableRate = models.CharField(max_length=250, blank = True, default = "None", null=True)
    market_rates = models.CharField(max_length=250, blank = True, default = "None", null=True)
    slug = models.SlugField(unique = True, default=uuid.uuid1)
    imageURL_forUse = models.CharField(max_length=250, blank = True, default = "None", null=True)



  





