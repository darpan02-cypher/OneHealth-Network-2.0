# accounts/models.py
from djongo.models import ObjectIdField
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = ObjectIdField(primary_key=True)  # Use ObjectIdField for MongoDB compatibility
    email = models.EmailField(unique=True)  # Ensure email is unique
    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = ['username']  # Keep username as a required field

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.username}"

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"Doctor: {self.user.username}"

class InsuranceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    policy_id = models.CharField(max_length=100)

    def __str__(self):
        return f"Insurance: {self.user.username}"
    
    
    



class HealthProfile(models.Model):
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name='health_profile')
    
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    height = models.FloatField(null=True, blank=True)  # in cm
    weight = models.FloatField(null=True, blank=True)  # in kg

    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)

    emergency_name = models.CharField(max_length=255, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)

    immunization = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    active_prescriptions = models.FileField(upload_to='prescriptions/', null=True, blank=True)
    medication_allergy_list = models.TextField(blank=True)
    current_problems_list = models.TextField(blank=True)
    lab_results = models.FileField(upload_to='lab_results/', null=True, blank=True)

    def __str__(self):
        return f"Health Profile of {self.patient.user.username}"

