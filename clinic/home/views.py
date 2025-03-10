from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, 'pages/index.html')

def home_page2(request):
    return render(request, 'others/index1.html')


def appoinment(request):
    return render(request, 'pages/appoinment.html')


def login(request):
    return render(request, 'pages/login.html')

def register(request):
    return render(request, 'pages/register.html')