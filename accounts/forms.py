from django import forms


class SignupForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('insurance', 'Insurance Provider')
    ])

class PatientSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField(required=False)
    medical_history = forms.CharField(widget=forms.Textarea, required=False)

class DoctorSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    hospital = forms.CharField(max_length=255)
    specialty = forms.CharField(max_length=100)

class InsuranceSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    company = forms.CharField(max_length=255)
    policy_id = forms.CharField(max_length=100)

class LoginForm(forms.Form):
    email = forms.EmailField()  # Use email for login
    password = forms.CharField(widget=forms.PasswordInput)




#health_profile_form.py
# accounts/forms.py
from django import forms
from .models import HealthProfile

class HealthProfileForm(forms.ModelForm):  # This form is for the HealthProfile model
    class Meta:
        model = HealthProfile
        fields = [
            'patient_name',  # Allow users to input a custom name
            'dob', 'gender', 'blood_group', 'height', 'weight',
            'allergies', 'chronic_conditions',
            'emergency_name', 'emergency_phone',
            'immunization', 'current_medications', 'active_prescriptions',
            'medication_allergy_list', 'current_problems_list', 'lab_results'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'blood_group': forms.Select(choices=[
                ('', 'Select'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
            ]),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'chronic_conditions': forms.Textarea(attrs={'rows': 2}),
            'immunization': forms.Textarea(attrs={'rows': 2}),
            'current_medications': forms.Textarea(attrs={'rows': 2}),
            'medication_allergy_list': forms.Textarea(attrs={'rows': 2}),
            'current_problems_list': forms.Textarea(attrs={'rows': 2}),
        }
        
        
        
           
#schedule_appointment_form.py
class ScheduleAppointmentForm(forms.ModelForm):
    #doctor = forms.ModelChoiceField(queryset=DoctorProfile.objects.all(), label="Select Doctor")
        
    doctor = forms.CharField(max_length=150, label="Select Doctor") # need to change this 
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Appointment Date")
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Appointment Time")
    reason = forms.CharField(widget=forms.Textarea, required=False, label="Reason for Appointment")
    notes = forms.CharField(widget=forms.Textarea, required=False, label="Additional Notes")

    class Meta:
        model = HealthProfile  # Replace with the correct model, e.g., Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'reason', 'notes']
