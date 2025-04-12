# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import (
    PatientSignupForm, DoctorSignupForm, InsuranceSignupForm, LoginForm
)
from .models import PatientProfile, DoctorProfile, InsuranceProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.db.utils import IntegrityError  # Import IntegrityError

from django.shortcuts import render, redirect
from .forms import HealthProfileForm
from .models import HealthProfile, PatientProfile
from django.contrib.auth.decorators import login_required


# Signup Views
def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            User = get_user_model()  # Get the custom user model
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password']
                    )
                    PatientProfile.objects.create(
                        user=user,
                        age=form.cleaned_data['age'],
                        medical_history=form.cleaned_data['medical_history']
                    )
                    login(request, user)
                    return redirect('patient_dashboard')
                except IntegrityError:
                    form.add_error('email', 'A user with this email already exists.')
                except Exception as e:
                    form.add_error(None, f"An unexpected error occurred: {str(e)}")
    else:
        form = PatientSignupForm()
    return render(request, 'patient/signup.html', {'form': form})

def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            User = get_user_model()  # Get the custom user model
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password']
                    )
                    DoctorProfile.objects.create(
                        user=user,
                        hospital=form.cleaned_data['hospital'],
                        specialty=form.cleaned_data['specialty']
                    )
                    login(request, user)
                    return redirect('doctor_dashboard')
                except IntegrityError:
                    form.add_error('email', 'A user with this email already exists.')
                except Exception as e:
                    form.add_error(None, f"An unexpected error occurred: {str(e)}")
    else:
        form = DoctorSignupForm()
    return render(request, 'doctor/signup.html', {'form': form})

def insurance_signup(request):
    if request.method == 'POST':
        form = InsuranceSignupForm(request.POST)
        if form.is_valid():
            User = get_user_model()  # Get the custom user model
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password']
                    )
                    InsuranceProfile.objects.create(
                        user=user,
                        company=form.cleaned_data['company'],
                        policy_id=form.cleaned_data['policy_id']
                    )
                    login(request, user)
                    return redirect('insurance_dashboard')
                except IntegrityError:
                    form.add_error('email', 'A user with this email already exists.')
                except Exception as e:
                    form.add_error(None, f"An unexpected error occurred: {str(e)}")
    else:
        form = InsuranceSignupForm()
    return render(request, 'insurance/signup.html', {'form': form})

# Generic login view
def user_login(request, role):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],  # Use email for authentication
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect(f'{role}_dashboard')  # e.g., patient_dashboard
            else:
                form.add_error(None, "Invalid email or password.")
        else:
            form.add_error(None, "Invalid form submission.")
    else:
        form = LoginForm()
    return render(request, f'{role}/login.html', {'form': form})

#dashboad for each

@login_required
def patient_dashboard(request):
    return render(request, 'patient/dashboard.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor/dashboard.html')

@login_required
def insurance_dashboard(request):
    return render(request, 'insurance/dashboard.html')

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
def contributors(request):
    return render(request, 'contributors.html')


def signup(request):
    return render(request, 'signup.html')

def login_view(request):  # Renamed from `login` to `login_view`
    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')


@login_required
def patient_health_profile(request):
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        return redirect('health_profile_view')  # Redirect to health profile form if no patient profile exists

    # Try to get existing health profile or create a new one
    health_profile, created = HealthProfile.objects.get_or_create(patient=patient_profile)

    if request.method == 'POST':
        form = HealthProfileForm(request.POST, request.FILES, instance=health_profile)
        if form.is_valid():
            form.save()
            return redirect('patient_health_profile')  # Redirect to the same page after saving
    else:
        form = HealthProfileForm(instance=health_profile)  # Pre-fill the form with existing data

    return render(request, 'patient/health_profile.html', {'form': form, 'health_profile': health_profile})


@login_required
def health_profile_view(request):
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        # Redirect to the patient dashboard with a message if no profile exists
        return redirect('patient_dashboard')

    # Try to get existing health profile
    health_profile, created = HealthProfile.objects.get_or_create(patient=patient_profile)

    if request.method == 'POST':
        form = HealthProfileForm(request.POST, request.FILES, instance=health_profile)
        if form.is_valid():
            form.instance.patient = patient_profile
            form.save()
            return redirect('patient_dashboard')  # Redirect after saving
    else:
        form = HealthProfileForm(instance=health_profile)

    return render(request, 'patient/health_profile_form.html', {'form': form})


