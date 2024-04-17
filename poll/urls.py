from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('vote/<int:id>/', views.vote, name='vote'),
    path('results/<int:id>/', views.results, name='results'),
]