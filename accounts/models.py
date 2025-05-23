# accounts/models.py
from djongo.models import ObjectIdField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
        if self.user:
            return f"Patient: {self.user.username}"
        return "Patient: (No User Associated)"

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
    patient_name = models.CharField(max_length=255, blank=True, null=True)
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
    
    
    
class ScheduleAppointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255)  # Store the doctor's name as a string
    appointment_date = models.DateTimeField()
    reason = models.TextField()

    def __str__(self):
        return f"Appointment for {self.patient.user.username} with {self.doctor_name} on {self.appointment_date}"

class InsuranceClaim(models.Model):
    policy_number = models.CharField(max_length=50)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim {self.policy_number} - {self.claim_amount}"

class Prescription(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prescriptions')
    doctor_name = models.CharField(max_length=255)  # Name of the doctor
    reason = models.TextField()  # Reason for the prescription
    file = models.FileField(upload_to='prescriptions/')  # File upload (photo, PDF, etc.)
    #uploaded_at = models.DateTimeField(auto_now_add=True)  # Date uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date uploaded

    def __str__(self):
        return f"Prescription for {self.patient.user.username} by {self.doctor_name} on {self.uploaded_at}"


