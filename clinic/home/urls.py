from django.contrib import admin
from django.urls import path, include
from .views import * 

urlpatterns = [
    path('', home_page, name='home'),
    path('2/', home_page2, name='home2'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),


    path('patient/old', patientDashboardOld, name='patientDashboardold'),
    path('patient/', patientDashboard, name='patient_dashboard'),
    path('p/view-appoinment/', viewAppoinment, name='viewAppoinment'),
    path('p/book-appoinment/', BookAppoinment, name='BookAppoinment'),
    path('p/document/', ViewDocument, name='ViewDocument'),
    path('message/', message, name='message'),





    path('doctor/', doctor, name='doctor'),
]