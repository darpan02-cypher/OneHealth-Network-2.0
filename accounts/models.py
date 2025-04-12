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
