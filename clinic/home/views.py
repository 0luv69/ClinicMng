from django.shortcuts import render

from django.contrib import messages


# Create your views here.


def home_page(request):
    messages.success(request, 'Welcome to our website!')
    return render(request, 'pages/index.html')

def home_page2(request):
    return render(request, 'others/index1.html')


def appoinment(request):
    return render(request, 'pages/appoinment.html')


def login(request):
    return render(request, 'pages/login.html')

def register(request):
    return render(request, 'pages/register.html')


def patientDashboard(request):
    return render(request, 'pages/patient/dashboard.html')


def viewAppoinment(request):
    return render(request, 'pages/patient/view_appoinment.html')
















def doctor(request):
    return render(request, 'pages/doctor-portal.html')