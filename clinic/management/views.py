from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from patient.models import *
from account.models import Profile


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


def ViewDoctors(request):
    patients = Profile.objects.filter(role='doctor').order_by('-created_at')
    

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
    return render(request, 'pages/management/view_doctors.html', context)



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
        return redirect('medicineMng')  # Avoid resubmitting form on reload

    context = {
        'medicines': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': per_page_options,
    }
    return render(request, 'pages/management/medicine_management.html', context)