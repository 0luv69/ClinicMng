from django.contrib import admin
from django.urls import path, include
from .views import * 

urlpatterns = [
    path('', home_page, name='home'),
    path('page2/', home_page2, name='home2'),
]