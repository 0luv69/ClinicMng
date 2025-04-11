from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages


def login(request):
    return render(request, 'pages/login.html')

def register(request):
    return render(request, 'pages/register.html')


def PostRegister(request):
    """Custom registration view that handles user sign-up."""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Validate password matching
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'account/register.html' )
        
        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'account/register.html', )
        
        # Create a new user; here username is set as the email for simplicity
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name,  # Saving full name as the first_name field
        )
        
        # The user’s Profile will be created automatically via signals
        
        # Automatically log the user in after registration
        login(request, user)
        return redirect('home')
    
    # For GET requests, simply render the registration template
    return render(request, 'account/register.html')


def Postlogin(requst):...