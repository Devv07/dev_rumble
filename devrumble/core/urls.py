from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.login_view, name='login'),  # Root URL goes to login
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]