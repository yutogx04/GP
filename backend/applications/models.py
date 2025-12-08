from django.db import models
from django.conf import settings
from django.utils import timezone


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'First Choice'),
        (2, 'Second Choice'),
        (3, 'Third Choice'),
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    offer = models.ForeignKey(
        'internships.InternshipOffer',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, null=True, blank=True)
    
    motivation_letter = models.TextField(blank=True)
    
    applied_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    score = models.FloatField(null=True, blank=True)
    
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['student', 'offer']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.offer.title}"
    
    @property
    def student_profile(self):
        return getattr(self.student, 'student_profile', None)


class ApplicationDocument(models.Model):
    """Additional documents submitted with application"""
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='application_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.application.student.full_name} - {self.name}"
