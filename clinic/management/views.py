from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from patient.models import Appointment
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
    profile = Profile.objects.get(user=request.user)
    qs = Appointment.objects.all().order_by('-created_at')[5:]

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
        'profile': profile,
        'appointments': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': per_page_options,
    }

    return render(request, 'pages/management/view_appointments.html', context)