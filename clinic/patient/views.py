from django.shortcuts import render

# Create your views here.


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

def p_profile(request):
    return render(request, 'pages/patient/profile.html')
