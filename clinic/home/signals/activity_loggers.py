from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import ActivityLog, Profile

@receiver(post_save)
def log_create_or_update(sender, instance, created, **kwargs):
    # Don't log the ActivityLog model itself
    if sender == ActivityLog:
        return

    # Ensure the model instance has a 'profile' or 'user' attribute
    profile = getattr(instance, 'profile', None)
    if not profile and hasattr(instance, 'user'):
        profile = getattr(instance.user, 'profile', None)

    if not profile or not isinstance(profile, Profile):
        return

    action_type = 'Created' if created else 'Updated'
    model_name = sender.__name__

    ActivityLog.objects.create(
        profile=profile,
        action=f"{action_type} {model_name}: {instance}"
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender == ActivityLog:
        return

    profile = getattr(instance, 'profile', None)
    if not profile and hasattr(instance, 'user'):
        profile = getattr(instance.user, 'profile', None)

    if not profile or not isinstance(profile, Profile):
        return

    model_name = sender.__name__

    ActivityLog.objects.create(
        profile=profile,
        action=f"Deleted {model_name}: {instance}"
    )
