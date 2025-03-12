from django.contrib import admin
from django.urls import path, include
from .views import * 

urlpatterns = [
    path('', home_page, name='home'),
    path('2/', home_page2, name='home2'),
    path('appoinment/', appoinment, name='appoinment'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),


    path('patient/', patientDashboard, name='patient'),
    path('p/viewAppoinment/', viewAppoinment, name='viewAppoinment'),



    path('doctor/', doctor, name='doctor'),
]