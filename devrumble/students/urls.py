from django.urls import path
from . import views

app_name = 'students'  # <-- important for reverse redirect

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # this is the dashboard
]
