from django.shortcuts import render
from doctor.models import *
from account.models import *
from patient.models import Appointment
from datetime import date

# Create your views here.

def doctorDashboard(request):
    return render(request, 'pages/doctor/dashboard.html')


def d_edit_schedules(request):
    profile: Profile = request.user.profile
    doctor: DoctorProfile = DoctorProfile.objects.get(profile = profile)
    date_slots: AppointmentDateSlot = AppointmentDateSlot.objects.filter(doctor = doctor)

    appoinment_data = {}
    for date_slot in date_slots:
        time_slots = AppointmentTimeSlot.objects.filter(appointment_date_slot = date_slot)

        time_slots_data = []
        for time_slot in time_slots:
            time_slots_data.append({
                'from_time': time_slot.from_time.strftime("%H:%M"),
                'to_time': time_slot.to_time.strftime("%H:%M"),
                'duration': time_slot.duration,
                'appointment_type': time_slot.appointment_type,
                'status': time_slot.status
            })

        date_str = date_slot.date.strftime("%Y-%m-%d")
        appoinment_data[date_str] = time_slots_data


    context = {
        'doctor' : doctor,
        'scheduleData': appoinment_data,
        'all_date_slots': date_slots
    }
    return render(request, 'pages/doctor/edit_schedules.html', context)


def ViewPatients(request):
    profile: Profile = request.user.profile
    doctor: DoctorProfile = DoctorProfile.objects.get(profile = profile)


    all_appoinemts: Appointment = Appointment.objects.filter(doctor = doctor)


    patientData= []

    for each_app in all_appoinemts:
        each_app: Appointment

        dob = each_app.profile.date_of_birth
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        patientData.append({
            "id": str(each_app.uuid),
            "image": each_app.profile.profile_pic.url,
            "name": each_app.profile.user.first_name,
            "patient_id": each_app.profile.user.username,
            "age": age,
            "gender": each_app.profile.gender,
            "appointment": each_app.appointment_date.strftime("%Y-%m-%d") + each_app.appointment_time_str ,
            "status": each_app.status ,
            "issue": each_app.appointment_type,
            "phone": each_app.profile.ph_number ,
            "email": each_app.profile.user.email ,
            "notes": each_app.reason,
            "file": each_app.file.url if each_app.file else ''

        })


    context = {
        "patientData": patientData
    }

    return render(request, 'pages/doctor/view_patients.html', context)


def OnlineSession(request):
    return render(request, 'pages/doctor/online_session.html')


def dSetting(request):
    return render(request, 'pages/doctor/setting.html')


def d_profile(request):
    return render(request, 'pages/doctor/profile.html')
