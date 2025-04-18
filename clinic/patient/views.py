from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.http import HttpRequest


from account.views import login_required_with_message
from django.contrib import messages
from datetime import datetime

from account.models import Profile, MedicalInfo
from patient.models import *

# --------------------------------------- Rendering Pages ------------------------------------------------------------


def patientDashboard(request):
    return render(request, 'pages/patient/dashboard.html')

def viewAppoinment(request):
    if request.method == 'POST':
        nick_name = request.POST.get('nick_name')
        doc_type = request.POST.get('doc_type')
        notes = request.POST.get('notes')

        files = request.FILES.get('document_file')  

        print (nick_name, doc_type, notes)

        profile: Profile = request.user.profile


        




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
def p_profile(request: HttpRequest):
    """Patient profile page view."""

    if request.method == 'GET':
        # Fetch the user's profile information
        profile: Profile = Profile.objects.get(user=request.user)

        # Pass the profile information to the template
        context = {
            'profile': profile,
        }

        return render(request, 'pages/patient/profile.html', context)
    
    else:
        try:
            profile: Profile = request.user.profile
            user: User = request.user

            # Handle profile picture
            profile_pic = request.FILES.get('profileImage')  
            if profile_pic:
                profile.profile_pic = profile_pic

            # Personal Info
            user.first_name = request.POST.get('full_name', '').strip()
            # user.email = request.POST.get('email', '').strip()
            profile.ph_number = request.POST.get('phone_number', '').strip()
            profile.address = request.POST.get('address', '').strip()

            dob_str = request.POST.get('date_of_birth', '').strip()
            if dob_str:
                try:
                    profile.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request, "Invalid date format for Date of Birth.")
                    return redirect('patient:profile')

            # Medical Info
            medical_info: MedicalInfo = profile.medical_info
            medical_info.blood_group = request.POST.get('blood_group', '').strip()
            medical_info.medical_conditions = request.POST.get('medicalConditions', '').strip()  # fixed name
            medical_info.allergies = request.POST.get('allergies', '').strip()  # make sure this field exists
            medical_info.on_going_medications = request.POST.get('medicines_on', '').strip()  # make sure this field exists

            # Emergency Contact
            profile.emg_contact_name = request.POST.get('emergency_contact_name', '').strip()
            profile.emg_contact_number = request.POST.get('emergency_contact_number', '').strip()
            profile.emg_contact_relation = request.POST.get('emergency_contact_relationship', '').strip()
            profile.emg_contact_address = request.POST.get('emergency_contact_address', '').strip()

            print("Emergency Contact:", profile.emg_contact_name, profile.emg_contact_number, profile.emg_contact_relation, profile.emg_contact_address)


            # Notification Settings
            profile.email_notification = 'emailNotifications' in request.POST
            profile.reminders = 'appointmentReminders' in request.POST


            medical_info.save()
            request.user.save()
            profile.save()

            messages.success(request, "Profile updated successfully.")
        except Exception as e:
            print(f"Error updating profile: {e}")
            messages.error(request, "An error occurred while updating your profile.")

        return redirect('patient:profile')






# --------------------------------------- Adding Logic on each pages ------------------------------------------------------------

