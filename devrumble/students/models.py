from django.db import models
from django.contrib.auth.models import User
from faculty.models import Course

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    courses = models.ManyToManyField(Course, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name