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
    path('p/join-v-call/', join_v_call, name='join_v_call'),
    path('p/lab-report/', labReport, name='labReport'),
    path('p/prescriptions/', prescriptions, name='prescriptions'),
    path('p/message/', message, name='p-message'),
    path('p/profile/', p_profile, name='p-profile'),







    path('doctor/', doctor, name='doctor_dashboard'),
    path('d/edit-schedules/', d_edit_schedules, name='d_edit_schedules'),
    path('d/view-patients/', ViewPatients, name='ViewPatients'),
    path('d/online-session/', OnlineSession, name='OnlineSession'),
    path('d/setting/', dSetting, name='dSetting'),
    path('d/profile/', d_profile, name='d-profile'),





    path('management/', management, name='management_dashboard'),



]