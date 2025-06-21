from django.contrib import admin
from django.urls import path, include
from doctor.views import * 
from management.views import *

app_name = 'management'


urlpatterns = [
    path('management/', management, name='management_dashboard'),
    path('', management, name='management_dashboard'),
    path('m/view-patients/', ViewPatients, name='ViewPatients_m'),
    path('m/view-doctors/', ViewPatients, name='ViewDoctors_m'),

    # path('m/d-profile/create/', create_doctor_profile, name='doctor_profile_create'),
    # path('m/d-profile/<slug:slug>/edit/', update_doctor_profile, name='doctor_profile_update'),
]