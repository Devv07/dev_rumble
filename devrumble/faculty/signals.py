from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import FacultyProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_faculty_profile(sender, instance, created, **kwargs):
    if created and instance.is_staff:  # or whatever condition identifies faculty
        FacultyProfile.objects.create(user=instance)