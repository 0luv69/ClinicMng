# Generated by Django 5.2.1 on 2025-06-15 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_calls_connection_conversation_conv_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='conv_type',
            field=models.CharField(choices=[('audio', 'Audio'), ('video', 'Video')], default='audio', max_length=10),
        ),
    ]
