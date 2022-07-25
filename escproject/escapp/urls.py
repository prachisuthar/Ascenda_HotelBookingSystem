from django.urls import path
from .views import *
from . import views 

app_name = "escapp"
urlpatterns = [
    path("", views.index, name = "index"),
    path("f1/", views.f1, name = "f1"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("booklogin/", BookLoginView.as_view(), name="booklogin"),
    path("booking/", BookingView.as_view(), name="booking"),

]