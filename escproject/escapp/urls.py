from django.urls import path
from .views import *
from . import views 

app_name = "escapp"
urlpatterns = [
    path("", views.index, name = "index"),
    path("f1/", views.f1, name = "f1"),


]