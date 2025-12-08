from django.db import models
from django.conf import settings

class Hospital(models.Model):
    TYPE_CHOICES = [
        ('chu', 'CHU (University Hospital Center)'),
        ('eph', 'Public Health Establishment'),
        ('clinic', 'Private Clinic'),
        ('office', 'Medical Office'),
    ]
    
    name = models.CharField(max_length=255)
    hospital_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    total_capacity = models.PositiveIntegerField(default=0)
    current_capacity = models.PositiveIntegerField(default=0)
    
    director = models.CharField(max_length=255, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    establishment_date = models.DateField(blank=True, null=True)
    
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def update_current_capacity(self):
        from internships.models import Internship
        active_internships = Internship.objects.filter(
            department__hospital=self,
            status__in=['in_progress', 'to_start']
        ).count()
        self.current_capacity = active_internships
        self.save(update_fields=['current_capacity'])
    
    @property
    def has_geolocation(self):
        """Check if hospital has latitude and longitude data"""
        return self.latitude is not None and self.longitude is not None
    
    @property
    def geolocation_dict(self):
        """Return geolocation as dictionary for API responses"""
        if self.has_geolocation:
            return {
                'latitude': self.latitude,
                'longitude': self.longitude
            }
        return None
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Hospitals"

class HospitalAdmin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='hospital_admin'
    )
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='admins')
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    appointment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.hospital.name}"
    
    class Meta:
        verbose_name_plural = "Hospital Administrators"