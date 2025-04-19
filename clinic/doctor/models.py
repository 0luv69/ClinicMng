from django.db import models
from django.utils.text import slugify
from account.models import Profile



class DoctorProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='doctor_profile')

    SPECIALIZATIONS = [
        ('general_medicine', 'General Medicine'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
        ('other', 'Other'),
    ]

    ALL_APPOINTMENT_TYPE =[
        ('general_consultation', 'General Consultation'),
        ('follow_up_visit', 'Follow-up Visit'),
        ('online_consultation', 'Online Consultation'),
        ('specialist_consultation', 'Specialist Consultation'),
    ]

    specialization = models.CharField(max_length=100, choices=SPECIALIZATIONS)
    appointment_type = appointment_type = models.JSONField(blank=True, null=True, default=list)#eg: ["General Consultation", "Follow-up Visit", "Online Consultation" ]


    qualifications = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField()
    license_number = models.CharField(max_length=100, blank=True)
    board_certified = models.BooleanField(default=False)
    languages_spoken = models.JSONField(blank=True, null=True)

    #rating & reviews
    star_rating = models.FloatField(null=True, blank=True)
    total_reviews =  models.IntegerField(null=True)

    #availability
    available_days = models.JSONField(blank=True, null=True)  # e.g., ["Monday", "Wednesday"]
    available_time_slots = models.JSONField(blank=True, null=True)  # e.g., [{"start": "10:00", "end": "14:00"}]

    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    accepts_new_patients = models.BooleanField(default=True)


    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = f"{self.profile.user.first_name}-{self.specialization}"
            self.slug = slugify(full_name)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Dr. {self.profile.user.first_name} ({self.specialization})"
    
