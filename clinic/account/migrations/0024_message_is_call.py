# Generated by Django 5.2.1 on 2025-06-30 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_rename_reset_password_token_profile_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_call',
            field=models.BooleanField(default=False),
        ),
    ]
