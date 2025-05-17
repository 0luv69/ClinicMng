from django.shortcuts import render
from doctor.models import *
from account.models import *
from patient.models import Appointment
from datetime import datetime, date
from datetime import timedelta, time
from collections import defaultdict

from django.http import JsonResponse
import json

# Create your views here.

def doctorDashboard(request):
    return render(request, 'pages/doctor/dashboard.html')


def d_edit_schedules(request):
    profile: Profile = request.user.profile
    doctor: DoctorProfile = DoctorProfile.objects.get(profile=profile)
    date_slots = AppointmentDateSlot.objects.filter(doctor=doctor).order_by('date')

    context = {
        'doctor' : doctor,
        'all_date_slots': date_slots
    }
    return render(request, 'pages/doctor/edit_schedules.html', context)


def get_dateTime_slots(request, start_date=None):
    profile: Profile = request.user.profile
    doctor: DoctorProfile = DoctorProfile.objects.get(profile=profile)
    date_slots = AppointmentDateSlot.objects.filter(doctor=doctor).order_by('date')
    Message = None
    # Parse start_date from string if provided, else use today
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            Message = "Invalid date format. Please use YYYY-MM-DD. For Now set start_date to today."
            start_date = date.today()
    else:
        start_date = date.today()

    date_range = [start_date + timedelta(days=i) for i in range(7)]

    # Preload all time slots for performance
    time_slots_all = AppointmentTimeSlot.objects.filter(
        appointment_date_slot__in=date_slots
    ).select_related('appointment_date_slot')

    # Map: { date: { hour: slot_data } }
    slot_lookup = defaultdict(dict)
    for ts in time_slots_all:
        date_str = ts.appointment_date_slot.date.strftime("%Y-%m-%d")
        hour = ts.from_time.hour
        slot_lookup[date_str][hour] = {
            'unique_id': ts.unique_id,
            'blank': 'false',
            'hour': hour,
            'from_time': ts.from_time.strftime("%H:%M"),
            'to_time': ts.to_time.strftime("%H:%M"),
            'duration': ts.duration,
            'appointment_type': ts.appointment_type,
            'status': ts.status,
        }

    # Construct output
    appointment_data = {}
    for each_date in date_range:
        date_str = each_date.strftime("%Y-%m-%d")
        appointment_data[date_str] = []

        for hour in range(8, 22):  # 8 to 21 inclusive
            slot_data = slot_lookup.get(date_str, {}).get(hour, {
                'unique_id': '',
                'blank': 'true',
                'hour': hour,
                'from_time': f"{hour}:00",
                'to_time': f"{hour + 1}:00",
                'duration': '30',  # default duration
                'appointment_type': 'General Checkup',  # default type
                'status': 'unavailable',  # default
            })
            appointment_data[date_str].append(slot_data)

    return JsonResponse({
        "success": True,
        "message": Message,
        "scheduleData": appointment_data
    }, safe=False)





def submit_dateTime_slots(request):
    if request.method != 'POST':
        return JsonResponse({'success': False,
                             'message': 'Only POST requests allowed'}, 
                             status=405)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    profile: Profile = request.user.profile
    doctor: DoctorProfile = DoctorProfile.objects.get(profile=profile)

    for date_str, slots in data.items():
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            continue  # skip invalid dates
        
        # Find or create date slot

        for slot in slots:
            # Skip if slot is already booked
            if slot.get('status') == 'booked':
                continue

            # Skip if slot is blank and remains unavailable (no need to update)
            if slot.get('blank') == 'true' and slot.get('status') == 'unavailable':
                continue

            date_slot, _ = AppointmentDateSlot.objects.get_or_create(doctor=doctor, date=date_obj)
            hour = slot.get('hour')
            status = slot.get('status', 'unavailable')
            duration = int(slot.get('duration', 30))

            # Time boundaries (duration is in minutes)
            from_time = time(hour, 0)
            to_time = (datetime.combine(date_obj, from_time) + timedelta(minutes=duration)).time()

            # Check if slot already exists
            existing_slot = AppointmentTimeSlot.objects.filter(
                appointment_date_slot=date_slot,
                from_time=from_time,
                to_time=to_time
            ).first()

            if existing_slot:
                # Update existing
                existing_slot.status = status
                existing_slot.duration = str(duration)
                existing_slot.save()
            else:
                # Create new
                AppointmentTimeSlot.objects.create(
                    appointment_date_slot=date_slot,
                    from_time=from_time,
                    to_time=to_time,
                    duration=str(duration),
                    status=status
                )


    return JsonResponse({'success': True, 'message': 'Schedule updated successfully'})




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
    profile: Profile = request.user.profile

    context = {
            'profile': profile,
    }
    return render(request, 'pages/doctor/profile.html', context)
