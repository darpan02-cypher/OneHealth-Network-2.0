from django.contrib import admin
from .models import User, PatientProfile, DoctorProfile, InsuranceProfile, HealthProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(User, BaseUserAdmin)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(InsuranceProfile)
admin.site.register(HealthProfile)
admin.site.site_header = "OneHealth Network Management System Admin"
admin.site.site_title = "HMS Admin Portal"
admin.site.index_title = "Welcome to OneHealth Network System"