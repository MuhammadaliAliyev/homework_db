from django.urls import path
from . import views

urlpatterns = [
    path('signup/patient/', views.PatientSignUpView.as_view(), name='patient_signup'),
    path('signup/doctor/', views.DoctorSignUpView.as_view(), name='doctor_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointment/create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('medical-record/create/<int:appointment_id>/', views.medical_record_create, name='medical_record_create'),
    path('doctor/edit-profile/', views.edit_doctor_profile, name='edit_doctor_profile'),
    path('patient/edit-profile/', views.edit_patient_profile, name='edit_patient_profile'),
]