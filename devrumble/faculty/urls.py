from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    path('', views.faculty_dashboard, name='faculty_dashboard'),
    # Add more URL patterns as needed
]