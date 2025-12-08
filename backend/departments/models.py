from django.db import models
from django.conf import settings

class Department(models.Model):
    hospital = models.ForeignKey(
        'hospitals.Hospital', 
        on_delete=models.CASCADE, 
        related_name='departments'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=5)
    specialty = models.CharField(max_length=255)
    
    internal_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, null=True)
    
    head = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='headed_departments'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.hospital.name}"
    
    def available_slots(self):
        from internships.models import Internship
        active_internships = Internship.objects.filter(
            offer__department=self,
            status__in=['in_progress', 'to_start']
        ).count()
        return max(0, self.capacity - active_internships)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Departments"