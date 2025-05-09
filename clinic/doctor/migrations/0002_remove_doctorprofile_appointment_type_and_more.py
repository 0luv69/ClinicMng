# Generated by Django 5.1.6 on 2025-04-19 10:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorprofile',
            name='appointment_type',
        ),
        migrations.RemoveField(
            model_name='doctorprofile',
            name='available_days',
        ),
        migrations.RemoveField(
            model_name='doctorprofile',
            name='available_time_slots',
        ),
        migrations.CreateModel(
            name='AppointmentSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_type', models.CharField(choices=[('general_consultation', 'General Consultation'), ('follow_up_visit', 'Follow-up Visit'), ('online_consultation', 'Online Consultation'), ('specialist_consultation', 'Specialist Consultation')], max_length=32)),
                ('date', models.DateField()),
                ('from_time', models.TimeField()),
                ('to_time', models.TimeField()),
                ('time_span', models.DurationField(default='01:00:00')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datetime_slots', to='doctor.doctorprofile')),
            ],
        ),
    ]
