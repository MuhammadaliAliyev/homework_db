from .views import base
from django.urls import path

urlpatterns = [
    path('', base, name='base'),
]