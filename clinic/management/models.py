from django.db import models
from account.models import Profile  # adjust import to your actual app name


class ManagerProfile(Profile):
    class Meta:
        proxy = True
        verbose_name = "Manager Profile"
        verbose_name_plural = "Manager Profiles"
        