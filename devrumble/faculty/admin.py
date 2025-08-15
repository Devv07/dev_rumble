# faculty/admin.py
from django.contrib import admin
from .models import FacultyProfile, Course, Assignment

admin.site.register(FacultyProfile)
admin.site.register(Course)
admin.site.register(Assignment)