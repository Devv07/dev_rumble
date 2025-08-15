from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})
    icon = models.CharField(max_length=50, default='fas fa-book')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class StudentCourseProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    location_icon = models.CharField(max_length=50, default='fa-map-marker-alt')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Discussion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    replies = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def user_initials(self):
        first_name = self.user.first_name or 'Unknown'
        last_name = self.user.last_name or ''
        return f"{first_name[0]}{last_name[0] if last_name else ''}"

    @property
    def time_ago(self):
        from django.utils.timesince import timesince
        return timesince(self.created_at)

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default='fa-file')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})

    def __str__(self):
        return self.title

class StudyGroup(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name='study_groups')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name