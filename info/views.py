from django.shortcuts import render
from .models import Department, Student, Tuition

# Create your views here.
def base(request):
    departments = Department.objects.all()
    students = Student.objects.all()
    tuitions = Tuition.objects.all()
    return render(request, 'base.html', {'departments': departments, 'students': students, 'tuitions': tuitions})