from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile_for_student(sender, instance, created, **kwargs):
    # Only create profile for student role
    if created and getattr(instance, "role", "") == "student":
        StudentProfile.objects.get_or_create(user=instance)
@receiver(post_save, sender=User)
def save_profile_for_student(sender, instance, **kwargs):
    # Ensure profile is saved when user is saved
    if getattr(instance, "role", "") == "student":
        try:
            profile = instance.student_profile
            profile.save()
        except StudentProfile.DoesNotExist:
            pass

@receiver(post_save, sender=User)
def create_profile_for_encadrant(sender, instance, created, **kwargs):
    # Only create profile for encadrant role
    if created and getattr(instance, "role", "") == "encadrant":
        from .models import EncadrantProfile
        EncadrantProfile.objects.get_or_create(user=instance)