from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django import forms
from doctor.models import DoctorProfile
from account.models import Profile
from account.views import login_required_with_message

# Create your views here.


def home_page(request):
    all_doc_profiles = DoctorProfile.objects.all()



    return render(request, 'pages/index.html', {'all_doc_profiles': all_doc_profiles})





def home_page2(request):
    return render(request, 'others/index1.html')
def patientDashboardOld(request):
    return render(request, 'others/patient_dashboard.html')

def terms(request):
    return render(request, 'pages/index.html')

def ViewPatients(request):
    return render(request, 'pages/doctor/view_patients.html')
def management(request):
    return render(request, 'pages/management/dashboard.html')














@login_required_with_message(login_url='account:login', message="You need to log in to view your Patient Details .")
def ViewPatientsRecords(request, patient_id):

    patient: Profile = Profile.objects.get(user__username = patient_id)

    lab_reports = patient.lab_reports_profile.all()
    prescriptions = patient.prescriptions.all()

    context = {
        "patient": patient,
        "patient_id": patient_id,
        "lab_reports": lab_reports,
        "prescriptions": prescriptions,
    }

    return render(request, 'pages/view_patients_records.html', context)