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
