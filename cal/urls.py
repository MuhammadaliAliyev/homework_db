from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/<int:event_id>/', views.event, name='event_edit'),
    path('event/new/', views.event, name='event_new'),
]