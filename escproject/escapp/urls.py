from django.urls import path
from .views import *
from . import views 

app_name = "escapp"
urlpatterns = [
    path("", views.index, name = "index"),
    path("hotellist/", HotelListView.as_view(), name="hotellist"),
    path("f1/", views.f1, name = "f1"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("booklogin/", BookLoginView.as_view(), name="booklogin"),
    path("booking/", BookingView.as_view(), name="booking"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("hotelinfo/<slug:slug>/", HotelInfoView.as_view(), name = "hotelinfo"),
    path("startbooking/<slug:slug>/", StartBooking.as_view(), name = "startbooking"),
    path("hotelinfo_map/", ViewMap.as_view(), name = "hotelinfo_map"),
    path("hotelrooms/", HotelRoomsView.as_view(), name="hotelrooms"),
    path("accountinfo/", AccountinfoView.as_view(), name="accountinfo"),



]