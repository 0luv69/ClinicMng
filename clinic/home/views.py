from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, 'index2.html')

def home_page2(request):
    return render(request, 'index.html')