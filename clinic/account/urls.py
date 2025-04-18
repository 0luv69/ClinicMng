from django.contrib import admin
from django.urls import path, include
from .views import * 


urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),


    path('register/submit/', PostRegister, name='PostRegister'),
    path('login/submit/', Postlogin, name='Postlogin'),

    path('forget-password/', login, name='forgetPassword'),

    path('user-logout/', logout, name='logout-user'),

    path('change-password/', change_password, name='changePassword'),

]