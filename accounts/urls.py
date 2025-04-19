from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Signup URLs
    path('signup/patient/', views.patient_signup, name='patient_signup'),
    path('signup/doctor/', views.doctor_signup, name='doctor_signup'),
    path('signup/insurance/', views.insurance_signup, name='insurance_signup'),

    # Login URLs
    path('login/patient/', views.user_login, {'role': 'patient'}, name='patient_login'),
    path('login/doctor/', views.user_login, {'role': 'doctor'}, name='doctor_login'),
    path('login/insurance/', views.user_login, {'role': 'insurance'}, name='insurance_login'),
    path('login/', views.login_view, name='login'),

    # Dashboard URLs
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/insurance/', views.insurance_dashboard, name='insurance_dashboard'),

    # Patient Health Profile
    path('dashboard/patient/health_profile/', views.patient_health_profile, name='patient_health_profile'),
    path('dashboard/patient/health_profile/view/', views.health_profile_view, name='health_profile_view'),
    path('dashboard/patient/schedule_appointment/', views.schedule_appointment, name='schedule_appointment'),
    


    # Logout URL
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    
    # Patient Health Profile
    path('dashboard/patient/health_profile/', views.patient_health_profile, name='patient_health_profile'),
]
