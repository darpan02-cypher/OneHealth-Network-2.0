# Generated by Django 3.2 on 2025-05-04 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_healthprofile_patient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleappointment',
            name='doctor',
            field=models.TextField(max_length=255),
        ),
    ]
