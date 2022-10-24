"""Acme_Support URL Configuration

this url configaration is used for connecting admin app 
all urls of the ADMIN are listed below which was connected to main project urls

the main connection of urls is setup in setting.py which we assigned to ROOT_URLCONF 
and in  settings.urls we included acme_admin app urls


"""
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    

]
