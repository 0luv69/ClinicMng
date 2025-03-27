from django.shortcuts import render

from django.contrib import messages


# Create your views here.


def home_page(request):
    return render(request, 'pages/index.html')

def home_page2(request):
    return render(request, 'others/index1.html')




def login(request):
    return render(request, 'pages/login.html')

def register(request):
    return render(request, 'pages/register.html')


def patientDashboardOld(request):
    return render(request, 'others/patient_dashboard.html')











def ViewPatients(request):
    return render(request, 'pages/doctor/view_patients.html')



def management(request):
    return render(request, 'pages/management/dashboard.html')