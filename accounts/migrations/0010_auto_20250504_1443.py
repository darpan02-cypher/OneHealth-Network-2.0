# Generated by Django 3.2 on 2025-05-04 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_doctor_scheduleappointment_doctor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleappointment',
            name='doctor_name',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=255)),
                ('reason', models.TextField()),
                ('file', models.FileField(upload_to='prescriptions/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='accounts.patientprofile')),
            ],
        ),
    ]
