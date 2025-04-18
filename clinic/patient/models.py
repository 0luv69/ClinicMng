from django.db import models
from django.contrib.auth.models import User


from account.models import Profile, MedicalInfo



class Documents(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="patients_documents")
    nick_name = models.CharField(max_length=255, blank=True)
    doc_type = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank= True)
    from_our_clinic = models.BooleanField(default=False)

    file = models.FileField(upload_to='patients_documents/', blank=True)


    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"{self.nick_name}"