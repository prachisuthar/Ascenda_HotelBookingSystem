from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(
    [SingaporeHotelList, KLHotelList, Customer, Booking, HotelList, Feature1, hotelNameToID, HotelPricesF2, Feature3_info, HotelRoomsInfo, HotelPicturesModel]
)