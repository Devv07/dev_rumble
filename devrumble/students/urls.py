# student/urls.py
from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]