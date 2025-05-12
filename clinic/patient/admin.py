from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Documents)
admin.site.register(Appointment)

admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(PrescriptionSchedule)






class LabReportParameterInline(admin.TabularInline):
    model = LabReportParameter
    extra = 1
    fields = ('parameter_name', 'result', 'reference_range', 'status')
    readonly_fields = ()
    # you can add show_change_link = True if you want clickable links to each parameter

@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'report_date', 'doctor', 'status')
    list_filter = ('status', 'report_type', 'report_date')
    search_fields = ('report_type', 'doctor', 'patient_profile')
    date_hierarchy = 'report_date'
    inlines = [LabReportParameterInline]
    fieldsets = (
        (None, {
            'fields': ('report_type', 'report_date', 'doctor', 'status', 'report_description', 'patient_profile')
        }),
    )