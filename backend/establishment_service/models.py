from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Establishment(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    admins = models.ManyToManyField(User, blank=True, related_name="managed_establishments")  # hospital admins

    def __str__(self):
        return self.name

class ServiceHospitalier(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    capacite_accueil = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} @ {self.establishment.name}"
