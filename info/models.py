from django.db import models

# Create your models here.
class Department(models.Model):
    dept_code = models.IntegerField(blank=False, primary_key=True)
    dept_name = models.CharField(max_length=30, blank=False)
    dept_chief = models.CharField(max_length=30)
    def __str__(self):
        return self.dept_name

class Student(models.Model):
    student_id = models.IntegerField(blank=False, primary_key=True)
    student_name = models.CharField(max_length=30)
    student_dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    registered_date = models.DateField(auto_now=True)
    def __str__(self):
        return self.student_name
    
class Tuition(models.Model):
    student_id = models.IntegerField(blank=False, primary_key=True)
    pay_date = models.DateField()
    amount = models.IntegerField()
    def __str__(self):
        return str(self.student_id)