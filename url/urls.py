from django.urls import path
from . import views

app_name = 'url'
urlpatterns = [
    path('', views.urlShort, name='index'),
    path('u/<str:slugs>',views.urlRedirect,name='redirect'),
]