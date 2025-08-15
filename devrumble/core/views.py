from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import datetime
from .models import Course, StudentCourseProgress, Event, Discussion, Resource, Assignment, StudyGroup

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_faculty = forms.BooleanField(label='Register as Faculty (Superadmin)', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_faculty']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if self.cleaned_data['is_faculty']:
            user.is_staff = True
            user.is_superuser = True
        user.save()
        return user

def login_view(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next', 'students:dashboard' if not request.user.is_superuser else 'faculty:faculty_dashboard')
        return redirect(next_url)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'students:dashboard' if not user.is_superuser else 'faculty:faculty_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('students:dashboard' if not request.user.is_superuser else 'faculty:faculty_dashboard')
    
    can_create_admin = not User.objects.filter(is_superuser=True).exists()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if can_create_admin and form.cleaned_data['is_faculty']:
                user.is_superuser = True
                user.is_staff = True
            elif form.cleaned_data['is_faculty'] and not can_create_admin:
                messages.error(request, 'Only one superadmin can be created initially. Contact the admin.')
                return render(request, 'registration/register.html', {'form': form, 'can_create_admin': can_create_admin})
            user.save()
            login(request, user)
            next_url = request.GET.get('next', 'students:dashboard' if not user.is_superuser else 'faculty:faculty_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'can_create_admin': can_create_admin})

def logout_view(request):
    logout(request)
    return redirect('core:login')

def redirect_to_dashboard(request):
    if request.user.is_authenticated:
        return redirect('students:dashboard')  # go to dashboard
    return redirect('core:login')