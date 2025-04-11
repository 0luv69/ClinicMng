from django.contrib import admin
from django.urls import path, include
from ..clinic_base.views import * 

urlpatterns = [
    path('', home_page, name='home'),
    path('2/', home_page2, name='home2'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),



    path('p/', include('patient.urls')),
    path('d/', include('doctor.urls')),
    # path('m/', include('management.urls')),



    path('patient/old', patientDashboardOld, name='patientDashboardold'),


    path('management/', management, name='management_dashboard'),
    path('m/view-patients/', ViewPatients, name='ViewPatients_m'),
    path('m/view-doctors/', ViewPatients, name='ViewDoctors_m'),


]