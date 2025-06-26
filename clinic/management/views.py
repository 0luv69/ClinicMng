from django.shortcuts import render, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from patient.models import *
from account.models import Profile

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib import messages
from django.db.models import ProtectedError

from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from django.db import transaction

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404


# Create your views here.
def management_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    appointments = Appointment.objects.all().order_by('-created_at')[:5]
    context = {
        'profile': profile,
        'appointments': appointments,
    }
    return render(request, 'pages/management/dashboard.html', context)

def ViewAppointmnets(request):
    qs = Appointment.objects.all().order_by('-created_at')
    # pull per_page from GET, default 10
    per_page = int(request.GET.get('per_page', 10))
    paginator = Paginator(qs, per_page)
    page_num = request.GET.get('page')

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # define your entries‑per‑page options here
    per_page_options = [10, 25, 50, 100]

    context = {
        'appointments': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': per_page_options,
    }

    return render(request, 'pages/management/view_appointments.html', context)


def ViewPatients(request):
    patients = Profile.objects.filter(role='patient').order_by('-created_at')
    

    # pull per_page from GET, default 10
    per_page = int(request.GET.get('per_page', 10))
    paginator = Paginator(patients, per_page)
    page_num = request.GET.get('page')

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # define your entries‑per‑page options here
    per_page_options = [10, 25, 50, 100]

    context = {
        'patients': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': per_page_options,
    }
    return render(request, 'pages/management/view_patients.html', context)


def update_profile(request, username):
    """
    View to update a patient's profile information
    """
    # Check permissions (only the user themselves or staff can update)
    if request.user.username != username and not request.user.is_staff:
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to update this profile'
        }, status=403)
    
    # Get the profile to update
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    try:

        if 'full_name' in request.POST:
            full_name = request.POST.get('full_name', '').strip()
            user.first_name = full_name
            user.save()

        # Handle profile picture if provided
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        
        # Update profile fields
        if 'ph_number' in request.POST:
            profile.ph_number = request.POST.get('ph_number', '')
        
        if 'address' in request.POST:
            profile.address = request.POST.get('address', '')
        
        if 'date_of_birth' in request.POST and request.POST.get('date_of_birth'):
            profile.date_of_birth = request.POST.get('date_of_birth')
        
        if 'gender' in request.POST:
            profile.gender = request.POST.get('gender', '')
        
        # Update notification settings
        profile.email_notification = 'email_notification' in request.POST
        profile.sms_notification = 'sms_notification' in request.POST
        profile.reminders = 'reminders' in request.POST

        profile.is_active = 'is_active' in request.POST
        profile.is_verified = 'is_verified' in request.POST
        
        # Save the profile
        profile.save()
        
        # Return success response with updated data
        return JsonResponse({
            'status': 'success',
            'message': 'Profile updated successfully',
            'profile_pic_url': profile.profile_pic.url if profile.profile_pic else None
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error updating profile: {str(e)}'
        }, status=400)

@require_POST
def update_medical_info(request, username):
    """
    View to update a patient's medical information
    """
    # Check permissions (only the user themselves or staff can update)
    if request.user.username != username and not request.user.is_staff:
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to update this medical information'
        }, status=403)
    
    # Get the medical info to update
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    # Get or create medical info if it doesn't exist
    medical_info, created = MedicalInfo.objects.get_or_create(profile=profile)
    
    try:
        # Update medical info fields
        if 'blood_group' in request.POST:
            medical_info.blood_group = request.POST.get('blood_group', '')
        
        if 'allergies' in request.POST:
            medical_info.allergies = request.POST.get('allergies', '')
        
        if 'medical_conditions' in request.POST:
            medical_info.medical_conditions = request.POST.get('medical_conditions', '')
        
        if 'on_going_medications' in request.POST:
            medical_info.on_going_medications = request.POST.get('on_going_medications', '')
        
        # Update emergency contact information
        if 'emg_contact_name' in request.POST:
            medical_info.emg_contact_name = request.POST.get('emg_contact_name', '')
        
        if 'emg_contact_number' in request.POST:
            medical_info.emg_contact_number = request.POST.get('emg_contact_number', '')
        
        if 'emg_contact_relation' in request.POST:
            medical_info.emg_contact_relation = request.POST.get('emg_contact_relation', '')
        
        if 'emg_contact_address' in request.POST:
            medical_info.emg_contact_address = request.POST.get('emg_contact_address', '')
        
        # Save the medical info
        medical_info.save()
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'message': 'Medical information updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error updating medical information: {str(e)}'
        }, status=400)





def ViewDoctors(request):
    doctors = Profile.objects.filter(role='doctor').order_by('-created_at')
    # pull per_page from GET, default 10
    per_page = int(request.GET.get('per_page', 10))
    paginator = Paginator(doctors, per_page)
    page_num = request.GET.get('page')

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # define your entries‑per‑page options here
    per_page_options = [10, 25, 50, 100]

    context = {
        'doctors': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': per_page_options,
    }
    return render(request, 'pages/management/view_doctors.html', context)


def EditDoctorInfo(request):
    """
    Handle doctor information updates based on request_type
    Supports: personal, professional, fees
    """
    try:
        # Parse JSON data
        data = json.loads(request.body.decode('utf-8'))
        request_type = data.get('request_type', '').strip()
        slug = data.get('slug', '').strip()

        # Validate required fields
        if not request_type:
            return JsonResponse({
                'success': False,
                'message': 'Missing request_type parameter'
            }, status=400)
            
        if not slug:
            return JsonResponse({
                'success': False,
                'message': 'Missing slug parameter'
            }, status=400)

        # Validate request type
        valid_types = ['personal', 'professional', 'fees']
        if request_type not in valid_types:
            return JsonResponse({
                'success': False,
                'message': f'Invalid request_type. Must be one of: {", ".join(valid_types)}'
            }, status=400)

        # Get doctor profile with error handling
        try:
            doctor_profile = DoctorProfile.objects.select_related(
                'profile__user'
            ).get(slug=slug)
        except DoctorProfile.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': f'Doctor with slug "{slug}" not found'
            }, status=404)

        # Log the edit attempt

        # Process different request types
        if request_type == 'personal':
            return handle_personal_update(doctor_profile, data, request.user)
        elif request_type == 'professional':
            return handle_professional_update(doctor_profile, data, request.user)
        elif request_type == 'fees':
            return handle_fees_update(doctor_profile, data, request.user)

    except json.JSONDecodeError as e:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data provided'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)


def handle_personal_update(doctor_profile, data, user):
    """Handle personal information updates with comprehensive validation"""
    try:
        with transaction.atomic():
            profile = doctor_profile.profile
            changes_made = []

            # Update active status
            if 'active' in data:
                active = bool(data['active'])
                if profile.is_active != active:
                    profile.is_active = active
                    changes_made.append('active status')

            # Update verified status
            if 'verified' in data:
                verified = bool(data['verified'])
                if profile.is_verified != verified:
                    profile.is_verified = verified
                    changes_made.append('verified status')

            # Update phone number with validation
            if 'phone' in data:
                phone = str(data['phone']).strip()
                if phone:
                    # Remove common phone formatting characters
                    clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
                    
                    # Basic phone validation (must be digits and reasonable length)
                    if not clean_phone.isdigit() or len(clean_phone) < 7 or len(clean_phone) > 15:
                        return JsonResponse({
                            'success': False,
                            'message': 'Phone number must be 7-15 digits long and contain only numbers'
                        }, status=400)
                    
                    if profile.ph_number != phone:
                        profile.ph_number = phone
                        changes_made.append('phone number')
                else:
                    if profile.ph_number:
                        profile.ph_number = ''
                        changes_made.append('phone number (cleared)')

            # Update address
            if 'address' in data:
                address = str(data['address']).strip()
                if len(address) > 255:  # Based on model field length
                    return JsonResponse({
                        'success': False,
                        'message': 'Address cannot exceed 255 characters'
                    }, status=400)
                
                if profile.address != address:
                    profile.address = address
                    changes_made.append('address')

            # Update gender with validation
            if 'gender' in data:
                gender = str(data['gender']).strip().lower()
                valid_genders = ['male', 'female', 'other', '']
                
                if gender not in valid_genders:
                    return JsonResponse({
                        'success': False,
                        'message': 'Gender must be one of: male, female, other, or empty'
                    }, status=400)
                
                if profile.gender != gender:
                    profile.gender = gender
                    changes_made.append('gender')

            # Update date of birth with comprehensive validation
            if 'date_of_birth' in data:
                dob_str = str(data['date_of_birth']).strip()
                
                if dob_str:
                    try:
                        # Parse date string (YYYY-MM-DD format)
                        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                        
                        # Validate date is reasonable
                        current_date = date.today()
                        min_birth_year = current_date.year - 100  # Max 100 years old
                        max_birth_year = current_date.year - 18   # Min 18 years old
                        
                        if dob.year < min_birth_year:
                            return JsonResponse({
                                'success': False,
                                'message': 'Birth year cannot be more than 100 years ago'
                            }, status=400)
                        
                        if dob.year > max_birth_year or dob > current_date:
                            return JsonResponse({
                                'success': False,
                                'message': 'Doctor must be at least 18 years old'
                            }, status=400)
                        
                        if profile.date_of_birth != dob:
                            profile.date_of_birth = dob
                            changes_made.append('date of birth')
                            
                    except ValueError:
                        return JsonResponse({
                            'success': False,
                            'message': 'Invalid date format. Please use YYYY-MM-DD format'
                        }, status=400)
                else:
                    if profile.date_of_birth:
                        profile.date_of_birth = None
                        changes_made.append('date of birth (cleared)')

            

            # Save changes if any were made
            if changes_made:
                profile.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Personal information updated successfully. Changes: {", ".join(changes_made)}',
                    'data': {
                        'phone': profile.ph_number,
                        'address': profile.address,
                        'gender': profile.gender,
                        'date_of_birth': profile.date_of_birth.strftime('%Y-%m-%d') if profile.date_of_birth else '',
                        'active': profile.is_active,
                        'verified': profile.is_verified,
                        'changes_made': changes_made
                    }
                })
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'No changes were made to personal information',
                    'data': {
                        'phone': profile.ph_number,
                        'address': profile.address,
                        'gender': profile.gender,
                        'date_of_birth': profile.date_of_birth.strftime('%Y-%m-%d') if profile.date_of_birth else '',
                        'active': profile.active,
                        'verified': profile.verified,
                        'changes_made': []
                    }
                })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating personal information: {str(e)}'
        }, status=500)

def handle_professional_update(doctor_profile, data, user):
    """Handle professional information updates with comprehensive validation"""
    try:
        with transaction.atomic():
            changes_made = []

            # Update specialization with validation
            if 'specialization' in data:
                specialization = str(data['specialization']).strip()
                valid_specializations = [choice[0] for choice in DoctorProfile.SPECIALIZATIONS]
                
                if specialization and specialization not in valid_specializations:
                    return JsonResponse({
                        'success': False,
                        'message': f'Invalid specialization. Must be one of: {", ".join(valid_specializations)}'
                    }, status=400)
                
                if doctor_profile.specialization != specialization:
                    doctor_profile.specialization = specialization
                    changes_made.append('specialization')

            # Update qualifications
            if 'qualifications' in data:
                qualifications = str(data['qualifications']).strip()
                
                if len(qualifications) > 2000:  # Reasonable limit for text field
                    return JsonResponse({
                        'success': False,
                        'message': 'Qualifications cannot exceed 2000 characters'
                    }, status=400)
                
                if doctor_profile.qualifications != qualifications:
                    doctor_profile.qualifications = qualifications
                    changes_made.append('qualifications')

            # Update experience years with validation
            if 'experience_years' in data:
                try:
                    experience = int(data['experience_years']) if data['experience_years'] is not None else 0
                    
                    if experience < 0:
                        return JsonResponse({
                            'success': False,
                            'message': 'Experience years cannot be negative'
                        }, status=400)
                    
                    if experience > 60:
                        return JsonResponse({
                            'success': False,
                            'message': 'Experience years cannot exceed 60 years'
                        }, status=400)
                    
                    if doctor_profile.experience_years != experience:
                        doctor_profile.experience_years = experience
                        changes_made.append('experience years')
                        
                except (ValueError, TypeError):
                    return JsonResponse({
                        'success': False,
                        'message': 'Experience years must be a valid number'
                    }, status=400)

            # Update license number
            if 'license_number' in data:
                license_number = str(data['license_number']).strip()
                
                if len(license_number) > 100:  # Based on model field length
                    return JsonResponse({
                        'success': False,
                        'message': 'License number cannot exceed 100 characters'
                    }, status=400)
                
                if doctor_profile.license_number != license_number:
                    doctor_profile.license_number = license_number
                    changes_made.append('license number')

            # Update board certification
            if 'board_certified' in data:
                board_certified = bool(data['board_certified'])
                
                if doctor_profile.board_certified != board_certified:
                    doctor_profile.board_certified = board_certified
                    changes_made.append('board certification status')

            # Update languages spoken with validation
            if 'languages_spoken' in data:
                languages = data['languages_spoken']
                
                if not isinstance(languages, list):
                    return JsonResponse({
                        'success': False,
                        'message': 'Languages must be provided as a list'
                    }, status=400)
                
                # Clean and validate languages
                clean_languages = []
                for lang in languages:
                    lang_str = str(lang).strip()
                    if lang_str:
                        if len(lang_str) > 50:  # Reasonable limit per language
                            return JsonResponse({
                                'success': False,
                                'message': 'Each language name cannot exceed 50 characters'
                            }, status=400)
                        clean_languages.append(lang_str)
                
                # Remove duplicates while preserving order
                seen = set()
                unique_languages = []
                for lang in clean_languages:
                    if lang.lower() not in seen:
                        seen.add(lang.lower())
                        unique_languages.append(lang)
                
                if len(unique_languages) > 10:  # Reasonable limit
                    return JsonResponse({
                        'success': False,
                        'message': 'Cannot specify more than 10 languages'
                    }, status=400)
                
                if doctor_profile.languages_spoken != unique_languages:
                    doctor_profile.languages_spoken = unique_languages
                    changes_made.append('languages spoken')

            # Save changes if any were made
            if changes_made:
                doctor_profile.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Professional information updated successfully. Changes: {", ".join(changes_made)}',
                    'data': {
                        'specialization': doctor_profile.get_specialization_display(),
                        'specialization_code': doctor_profile.specialization,
                        'qualifications': doctor_profile.qualifications,
                        'experience_years': doctor_profile.experience_years,
                        'license_number': doctor_profile.license_number,
                        'board_certified': doctor_profile.board_certified,
                        'languages_spoken': doctor_profile.languages_spoken,
                        'changes_made': changes_made
                    }
                })
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'No changes were made to professional information',
                    'data': {
                        'specialization': doctor_profile.get_specialization_display(),
                        'specialization_code': doctor_profile.specialization,
                        'qualifications': doctor_profile.qualifications,
                        'experience_years': doctor_profile.experience_years,
                        'license_number': doctor_profile.license_number,
                        'board_certified': doctor_profile.board_certified,
                        'languages_spoken': doctor_profile.languages_spoken,
                        'changes_made': []
                    }
                })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating professional information: {str(e)}'
        }, status=500)


def handle_fees_update(doctor_profile, data, user):
    """Handle fees and availability updates with comprehensive validation"""
    try:
        with transaction.atomic():
            changes_made = []

            # Update consultation fees with validation
            if 'fees' in data:
                try:
                    fees = Decimal(str(data['fees'])) if data['fees'] is not None else Decimal('0.00')
                    
                    if fees < 0:
                        return JsonResponse({
                            'success': False,
                            'message': 'Consultation fees cannot be negative'
                        }, status=400)
                    
                    # Check maximum value based on model definition (max_digits=10, decimal_places=2)
                    if fees >= Decimal('100000000.00'):  # 99,999,999.99 is the max
                        return JsonResponse({
                            'success': False,
                            'message': 'Consultation fees amount is too large (maximum: $99,999,999.99)'
                        }, status=400)
                    
                    # Validate decimal places
                    if fees.as_tuple().exponent < -2:
                        return JsonResponse({
                            'success': False,
                            'message': 'Consultation fees can have at most 2 decimal places'
                        }, status=400)
                    
                    if doctor_profile.fees != fees:
                        doctor_profile.fees = fees
                        changes_made.append('consultation fees')
                        
                except (InvalidOperation, ValueError, TypeError) as e:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid fees amount. Please enter a valid number'
                    }, status=400)

            # Update accepts new patients status
            if 'accepts_new_patients' in data:
                accepts_new = bool(data['accepts_new_patients'])
                
                if doctor_profile.accepts_new_patients != accepts_new:
                    doctor_profile.accepts_new_patients = accepts_new
                    changes_made.append('new patient acceptance status')

            # Save changes if any were made
            if changes_made:
                doctor_profile.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Fees and availability updated successfully. Changes: {", ".join(changes_made)}',
                    'data': {
                        'fees': str(doctor_profile.fees),
                        'accepts_new_patients': doctor_profile.accepts_new_patients,
                        'changes_made': changes_made
                    }
                })
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'No changes were made to fees and availability',
                    'data': {
                        'fees': str(doctor_profile.fees),
                        'accepts_new_patients': doctor_profile.accepts_new_patients,
                        'changes_made': []
                    }
                })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating fees and availability: {str(e)}'
        }, status=500)


def medicineMng(request):
    medicines = Medicine.objects.all().order_by('-created_at')

    # pull per_page from GET, default 10
    per_page = int(request.GET.get('per_page', 10))
    paginator = Paginator(medicines, per_page)
    page_num = request.GET.get('page')
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Define your entries-per-page options here
    per_page_options = [10, 25, 50, 100]

    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        generic_name = request.POST.get('generic_name')
        brand_name = request.POST.get('brand_name')
        manufacturer = request.POST.get('manufacturer')
        description = request.POST.get('description')
        default_dosage = request.POST.get('default_dosage')
        default_frequency = request.POST.get('default_frequency')
        instructions = request.POST.get('instructions')
        side_effects = request.POST.get('side_effects')

        Medicine.objects.create(
            name=name,
            generic_name=generic_name,
            brand_name=brand_name,
            manufacturer=manufacturer,
            description=description,
            default_dosage=default_dosage,
            default_frequency=default_frequency,
            instructions=instructions,
            side_effects=side_effects
        )
        return redirect('management:medicineMng')  # Avoid resubmitting form on reload

    context = {
        'medicines': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': per_page_options,
    }
    return render(request, 'pages/management/medicine_management.html', context)


def delete_medicine(request, medicine_uuid):
    try:
        medicine = Medicine.objects.get(uuid=medicine_uuid)
        medicine.delete()
        messages.success(request, 'Medicine deleted successfully.')
    except Medicine.DoesNotExist:
        messages.error(request, 'Medicine not found.')
    except ProtectedError:
        messages.error(request, 'Cannot delete this medicine as it is referenced in prescriptions.')
    except Exception as e:
        messages.error(request, 'An unexpected error occurred.')
    return redirect('management:medicineMng')
