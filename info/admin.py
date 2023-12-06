from django.contrib import admin
from .models import Department, Student, Tuition
# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_code', 'dept_name', 'dept_chief')
    ordering = ('dept_code',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'student_dept', 'registered_date')
    ordering = ('student_id',)

class TuitionAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'pay_date', 'amount')
    ordering = ('student_id',)

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Tuition, TuitionAdmin)
