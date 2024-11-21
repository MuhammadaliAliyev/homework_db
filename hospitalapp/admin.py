
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Doctor, Patient, MedicalRecord, Appointment

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    list_filter = BaseUserAdmin.list_filter + ('userprofile__user_type',)
    
    def get_user_type(self, obj):
        return obj.userprofile.user_type
    get_user_type.short_description = 'User Type'


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specialization', 'license_number', 'experience_years')
    search_fields = ('user_profile__user__first_name', 'user_profile__user__last_name', 'specialization')
    list_filter = ('specialization',)
    
    def get_full_name(self, obj):
        return f"Dr. {obj.user_profile.user.get_full_name()}"
    get_full_name.short_description = 'Doctor Name'


class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'blood_group', 'emergency_contact')
    search_fields = ('user_profile__user__first_name', 'user_profile__user__last_name', 'blood_group')
    list_filter = ('blood_group',)
    
    def get_full_name(self, obj):
        return obj.user_profile.user.get_full_name()
    get_full_name.short_description = 'Patient Name'

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'date_created')
    list_filter = ('date_created', 'doctor')
    search_fields = ('patient__user_profile__user__first_name', 'patient__user_profile__user__last_name',
                    'doctor__user_profile__user__first_name', 'doctor__user_profile__user__last_name',
                    'diagnosis')
    date_hierarchy = 'date_created'
    
    def get_patient_name(self, obj):
        return obj.patient.user_profile.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user_profile.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'date_time', 'status')
    list_filter = ('status', 'date_time')
    search_fields = ('patient__user_profile__user__first_name', 'patient__user_profile__user__last_name',
                    'doctor__user_profile__user__first_name', 'doctor__user_profile__user__last_name')
    date_hierarchy = 'date_time'
    
    def get_patient_name(self, obj):
        return obj.patient.user_profile.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user_profile.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'

# Unregister the default User admin and register with custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register all other models
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Appointment, AppointmentAdmin)