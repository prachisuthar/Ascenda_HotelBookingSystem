from django.db import models
import json
from django.contrib.auth.models import User 
import uuid
from datetime import datetime
# Create your models here.

class Feature1(models.Model):
    country = models.CharField(max_length=250, blank=True, default="-")
    uid = models.CharField(max_length=250, blank=True)
    guests_number = models.PositiveIntegerField(blank=True, default = 3)
    rooms_number = models.PositiveIntegerField(blank=True, default = 3)
    start_date = models.DateField(blank=True, default = "2020-10-10")
    end_date = models.DateField(blank=True, default = "2020-11-11")


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