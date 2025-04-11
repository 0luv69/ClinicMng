from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from account.models import Profile
from account.views import login_required_with_message
from django.contrib import messages


# --------------------------------------- Rendering Pages ------------------------------------------------------------


def patientDashboard(request):
    return render(request, 'pages/patient/dashboard.html')

def viewAppoinment(request):
    return render(request, 'pages/patient/view_appoinment.html')

def BookAppoinment(request):
    return render(request, 'pages/patient/book_appoinment.html')

def ViewDocument(request):
    return render(request, 'pages/patient/view_document.html')

def join_v_call(request):
    return render(request, 'pages/patient/join-v-call.html')

def message(request):
    return render(request, 'pages/patient/message.html')

def labReport(request):
    return render(request, 'pages/patient/lab_report.html')

def prescriptions(request):
    return render(request, 'pages/patient/prescriptions.html')

@login_required_with_message(login_url='account:login', message="You need to log in to access Profile page.")
def p_profile(request):
    """Patient profile page view."""

    if request.method == 'GET':
        # Fetch the user's profile information
        profile = Profile.objects.get(user=request.user)

        # Pass the profile information to the template
        context = {
            'profile': profile,
        }

        return render(request, 'pages/patient/profile.html', context)
    return render(request, 'pages/patient/profile.html')




# --------------------------------------- Adding Logic on each pages ------------------------------------------------------------

@login_required_with_message(login_url='account:login', message="You need to log in to access this page.")
def edit_profile(request):
    if request.method == 'POST':

        profile_pic = request.FILES.get('profile_pic')



        # personal information
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')


        # medical information
        blood_type = request.POST.get('blood_type')
        medical_history = request.POST.get('medical_conditions')
        
        # emergency contact information
        emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact_number = request.POST.get('emergency_contact_number')
        emergency_contact_relationship = request.POST.get('emergency_contact_relationship')





        if profile_pic:
            request.user.profile.profile_picture = profile_pic
            request.user.profile.save()


        return redirect('patient:p-profile')