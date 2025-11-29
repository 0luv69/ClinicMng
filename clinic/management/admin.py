from django.contrib import admin
from django.utils.html import format_html

from account.models import Profile  # if you need it
from .models import ManagerProfile


@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_username',
        'user_full_name',
        'profile_image_tag',
        'user_email',
        'gender',
        'is_active',
        'is_verified',
        'created_at',
        'updated_at',
    )
    list_filter = ('gender', 'is_active', 'is_verified', 'created_at')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'address',
    )
    readonly_fields = ('created_at', 'updated_at', 'profile_image_tag', 'user_email')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Info', {
            'fields': ('profile_pic', 'profile_image_tag', 'user_email', 'address', 'date_of_birth', 'gender')
        }),
        ('Token Info', {
            'fields': ('token', 'token_expiry',)
        }),
        ('Notifications', {
            'fields': ('email_notification', 'sms_notification', 'reminders')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified', 'created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        """
        Limit this admin to only profiles with role='management'.
        Adjust value based on your USER_ROLES choices.
        """
        qs = super().get_queryset(request)
        return qs.filter(role='management')  # or 'manager' if that's your value

    # ----- helper display methods (same pattern as in ProfileAdmin) -----

    def user_username(self, obj):
        return obj.user.username if obj and getattr(obj, 'user', None) else "-"
    user_username.short_description = 'Username'
    user_username.admin_order_field = 'user__username'

    def user_full_name(self, obj):
        if not obj or not getattr(obj, 'user', None):
            return "-"
        return f"{obj.user.first_name} {obj.user.last_name}"
    user_full_name.short_description = 'Full Name'

    def user_email(self, obj):
        if not obj or not getattr(obj, 'user', None):
            return "-"
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def profile_image_tag(self, obj):
        if obj and getattr(obj, 'profile_pic', None):
            return format_html(
                '<img src="{}" style="height: 40px; width: 40px; border-radius: 5px;" />',
                obj.profile_pic.url
            )
        return "-"
    profile_image_tag.short_description = "Profile Picture"