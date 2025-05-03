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
from .models import InsuranceClaim
from .forms import ScheduleAppointmentForm  # Correct import statement
from .models import ScheduleAppointment  # Import the ScheduleAppointment model

from datetime import datetime, timedelta  # Import datetime and timedelta

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
                username=form.cleaned_data['email'],  # Use email for authentication
                password=form.cleaned_data['password']
            )
            if user is not None:
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
    patients = PatientProfile.objects.all()  # Fetch all patients

    # Filter by patient_id if provided
    patient_id = request.GET.get('patient_id')
    if patient_id:
        patients = patients.filter(id=patient_id)

    return render(request, 'doctor/dashboard.html', {'patients': patients})

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




# Patient Health Profile
@login_required
def patient_health_profile(request):
    # Ensure the PatientProfile exists for the logged-in user
    patient_profile = PatientProfile.objects.get_or_create(user=request.user)[0]

    try:
        # Check if the health profile exists
        health_profile = HealthProfile.objects.get(patient=patient_profile)
    except HealthProfile.DoesNotExist:
        health_profile = None

    if request.method == 'POST':
        form = HealthProfileForm(request.POST, request.FILES, instance=health_profile)
        if form.is_valid():
            health_profile = form.save(commit=False)
            health_profile.patient = patient_profile
            # Ensure patient_name is set to a valid string
            if not health_profile.patient_name:
                health_profile.patient_name = request.user.username  # Default to username if not provided
            health_profile.save()
            return redirect('patient_dashboard')
    else:
        form = HealthProfileForm(instance=health_profile)

    return render(request, 'patient/health_profile_form.html', {
        'form': form,
        'is_edit': health_profile is not None  # Pass a flag to indicate edit mode
    })

@login_required
def health_profile_view(request):
    try:
        # Fetch the health profile for the logged-in patient
        health_profile = HealthProfile.objects.get(patient__user=request.user)
    except HealthProfile.DoesNotExist:
        return redirect('patient_health_profile')  # Redirect to the form if no profile exists

    if request.method == 'POST':
        form = HealthProfileForm(request.POST, request.FILES, instance=health_profile)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')
    else:
        form = HealthProfileForm(instance=health_profile)

    return render(request, 'patient/health_profile_view.html', {
        'form': form,
        'is_edit': True  # Always in edit mode for this view
    })

@login_required
def view_health_profile(request):
    try:
        # Fetch the health profile for the logged-in patient
        health_profile = HealthProfile.objects.get(patient__user=request.user)
    except HealthProfile.DoesNotExist:
        return redirect('patient_health_profile')  # Redirect to the form if no profile exists

    return render(request, 'patient/view_health_profile.html', {
        'health_profile': health_profile
    })

@login_required
def view_patient_health_profile(request, patient_id):
    try:
        # Fetch the patient profile using the provided patient_id
        patient_profile = PatientProfile.objects.get(id=patient_id)
        # Fetch the health profile associated with the patient
        health_profile = HealthProfile.objects.get(patient=patient_profile)
    except PatientProfile.DoesNotExist:
        return HttpResponse("Patient not found.", status=404)
    except HealthProfile.DoesNotExist:
        return HttpResponse("Health profile not found for this patient.", status=404)

    return render(request, 'doctor/view_patient_health_profile.html', {
        'patient_profile': patient_profile,
        'health_profile': health_profile
    })

#schedule appointment
@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = ScheduleAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = PatientProfile.objects.get(user=request.user)
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = ScheduleAppointmentForm()
    return render(request, 'patient/schedule_appointments.html', {'form': form})

#static appointment page
def static_appointment_page(request):
    return render(request, 'patient/static_appointment_page.html')

# Claim Insurance
def claim_insurance(request):
    if request.method == 'POST':
        policy_number = request.POST['policy_number']
        claim_amount = request.POST['claim_amount']

        reason = request.POST['reason']
        
        # Save the claim to the database
        InsuranceClaim.objects.create(
            policy_number=policy_number,
            claim_amount=claim_amount,
            reason=reason
        )
        return HttpResponse("Insurance claim submitted successfully!")
    return render(request, 'patient/claim_insurance_form.html')

# Check Appointments
@login_required
def check_appointments(request):
    # Fetch appointments for the logged-in user (assuming they are a doctor)
    now = datetime.now()
    today_start = datetime.combine(now.date(), datetime.min.time())
    today_end = datetime.combine(now.date(), datetime.max.time())

    # Filter appointments manually
    upcoming_appointments = ScheduleAppointment.objects.filter(
        doctor__user=request.user, appointment_date__gt=now
    ).order_by('appointment_date')
    past_appointments = ScheduleAppointment.objects.filter(
        doctor__user=request.user, appointment_date__lt=today_start
    ).order_by('-appointment_date')
    present_appointments = ScheduleAppointment.objects.filter(
        doctor__user=request.user, appointment_date__gte=today_start, appointment_date__lte=today_end
    ).order_by('appointment_date')

    return render(request, 'doctor/check_appointments.html', {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'present_appointments': present_appointments,
    })






