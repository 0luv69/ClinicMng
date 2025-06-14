# Generated by Django 5.2.1 on 2025-06-15 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_callconnection_calls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calls',
            name='connection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convosation_calls', to='account.conversation'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='conv_type',
            field=models.CharField(choices=[('audio', 'Audio'), ('video', 'Video'), ('message', 'Message')], default='message', max_length=10),
        ),
        migrations.AddField(
            model_name='conversation',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='status',
            field=models.CharField(choices=[('initiated', 'Initiated'), ('active', 'Active'), ('requested', 'Requested'), ('rejected', 'Rejected'), ('archived', 'Archived'), ('deleted', 'Deleted')], default='requested', max_length=10),
        ),
        migrations.DeleteModel(
            name='CallConnection',
        ),
    ]
