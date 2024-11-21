from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .models import *
from .forms import *

@login_required
def dashboard(request):

    if request.user.is_superuser:
        return redirect('admin:index')

    user_profile = request.user.userprofile
    
    if user_profile.user_type == 'doctor':
        doctor = Doctor.objects.get(user_profile=user_profile)
        print(doctor.user_profile.__getattribute__('phone_number'))
        appointments = Appointment.objects.filter(doctor=doctor)
        medical_records = MedicalRecord.objects.filter(doctor=doctor)
        
        context = {
            'doctor': doctor,
            'appointments': appointments,
            'medical_records': medical_records,
        }
        return render(request, 'doctor/dashboard.html', context)
    
    else:  # Patient
        patient = Patient.objects.get(user_profile=user_profile)
        appointments = Appointment.objects.filter(patient=patient)
        medical_records = MedicalRecord.objects.filter(patient=patient)
        
        context = {
            'patient': patient,
            'appointments': appointments,
            'medical_records': medical_records,
        }
        return render(request, 'patient/dashboard.html', context)

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        user.userprofile.user_type = 'patient'
        user.userprofile.save()
        Patient.objects.create(user_profile=user.userprofile)
        return super().form_valid(form)

class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        user.userprofile.user_type = 'doctor'
        user.userprofile.save()
        Doctor.objects.create(
            user_profile=user.userprofile,
            specialization=form.cleaned_data.get('specialization'),
            license_number=form.cleaned_data.get('license_number')
        )
        return super().form_valid(form)

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment/create.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.patient = self.request.user.userprofile.patient
        return super().form_valid(form)

@login_required
def medical_record_create(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = appointment.patient
            medical_record.doctor = appointment.doctor
            medical_record.save()
            appointment.status = 'completed'
            appointment.save()
            return redirect('dashboard')
    else:
        form = MedicalRecordForm()
    
    return render(request, 'medical_record/create.html', {
        'form': form,
        'appointment': appointment
    })

@login_required
def edit_doctor_profile(request):
    user = request.user
    doctor = Doctor.objects.get(user_profile=user.userprofile)
    
    if request.method == 'POST':
        form = DoctorChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            doctor.save()
            return redirect('dashboard')
    else:
        form = DoctorChangeForm(instance=user)
    
    return render(request, 'doctor/edit_profile.html', {
        'form': form
    })

@login_required
def edit_patient_profile(request):
    user = request.user
    patient = Patient.objects.get(user_profile=user.userprofile)
    
    if request.method == 'POST':
        form = PatientChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            patient.save()
            return redirect('dashboard')
    else:
        form = PatientChangeForm(instance=user)
    
    return render(request, 'patient/edit_profile.html', {
        'form': form
    })