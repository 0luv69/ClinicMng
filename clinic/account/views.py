from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from functools import wraps
from datetime import datetime



app_name = 'account'




def login_required_with_message(function=None, login_url=None, message=None):
    """
    Custom decorator for views that checks if the user is logged in.
    Adds a message if the user is redirected to the login page.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print("Inside the decorator")
            if not request.user.is_authenticated:
                if message:
                    messages.warning(request, message)
                return redirect(login_url or 'account:login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator










def login_page(request):
    return render(request, 'pages/login.html')

def register_page(request):
    return render(request, 'pages/register.html')


def PostRegister(request):
    """Custom registration view that handles user sign-up."""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password_confirmation')

        # Validate required fields
        if not full_name or not email or not password or not password2:
            messages.error(request, "All fields are required.")
            return redirect('account:register')
        
        # Validate password matching
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('account:register')
        
        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('account:register')

        
        # Create a new user; here username is set as the email for simplicity
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')  # Format: YYYYMMDDHHMMSS
        counter = str(User.objects.count() + 1).zfill(8)  # Ensure at least 6 digits
        username = f"NCMS-{current_time}-{counter}"
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name,  # Saving full name as the first_name field
        )
        # The user’s Profile will be created automatically via signals

        messages.success(request, "Registration successful.")
        
        
        # Automatically log the user in after registration
        login(request, user)
        return redirect('patient:p-profile')
    
    return redirect('account:register')



def Postlogin(request):
    """Custom login view that uses email and password."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('account:login')
        
        # Look up the user using the provided email
        try:
            user_obj = User.objects.get(email=email)
            # Authenticate using the username and password
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            messages.success(request, "Login successful.")

            role = request.user.profile.role
            if role == 'doctor':
                return redirect('doctor:d-profile')
            elif role == 'patient':
                return redirect('patient:p-profile')
            elif role == 'management':
                return redirect('home')

        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('account:login')

    
    # If GET request, simply render the login template
    return redirect('account:login')
