from django.contrib import admin
from django.urls import path, include
from .views import * 


urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),


    path('register/submit/', PostRegister, name='PostRegister'),
    path('login/submit/', Postlogin, name='Postlogin'),

    path('forget-password/', login, name='forget-password'),

]