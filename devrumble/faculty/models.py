from django.db import models

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    office_location = models.CharField(max_length=50)
    office_hours = models.TextField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"

class Course(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.code} - {self.title}"

# Add more models as needed for your smart campus features
