from django.contrib import admin
from django.urls import path, include
from doctor.views import * 
from management.views import *

app_name = 'management'


urlpatterns = [
    path('management/', management_dashboard, name='management_dashboard'),
    path('', management_dashboard, name='management_dashboard'),
    path('view-appointments/', ViewAppointmnets, name='viewAppointment'),
    path('view-patients/', ViewPatients, name='ViewPatients'),
    path('view-doctors/', ViewDoctors, name='ViewDoctors'),

    path('medicine-mng/', medicineMng, name='medicineMng'),

    # path('m/d-profile/create/', create_doctor_profile, name='doctor_profile_create'),
    # path('m/d-profile/<slug:slug>/edit/', update_doctor_profile, name='doctor_profile_update'),
]