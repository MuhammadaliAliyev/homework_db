from django.contrib import admin
from .models import Poll
# Register your models here.

class PollAdmin(admin.ModelAdmin):
    list_display = ['id','question', 'created_at', 'option_one', 'option_two', 'option_three']
admin.site.register(Poll, PollAdmin)