from django.urls import path
from .views import *
from . import views 

app_name = "escapp"
urlpatterns = [
    path("", views.index, name = "index"),
    path("index2/", views.index2, name = "index2"),
    # path("", HomeView.as_view(), name='index'),
    path("hotellist/", HotelListView.as_view(), name="hotellist"),
    path("f1/", views.f1, name = "f1"),
    # path("hotellist/", views.hotel_get_context_data, name = "hotellist"),
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
    path("deleteaccount/", CheckDeleteAccountView.as_view(), name="deleteaccountcheck"),
    path("confirmdelete/", ConfirmDeleteView.as_view(), name="confirmdelete"),
    path("confirmtransaction/", ConfirmTransactionView.as_view(), name="confirmtransaction"),
    path("bookingdone/", BookingDoneView.as_view(), name="bookingdone"),
    path("deleteuser/", DeleteUserView.as_view(), name="deleteuser"),
    path("f2/", views.f2, name = "f2"),
    path("hotelsearched/", HotelInfoView_V2.as_view(), name="hotelsearched"),
    path("bookinghistory/", views.BookingHistory, name = "bookinghistory"),





]