"""
Digital Signature model for storing captured signatures.
Signatures are stored as Base64-encoded PNG data.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Signature(models.Model):
    """Stores digital signatures captured from SignaturePad component."""
    
    SIGNER_TYPES = [
        ('supervisor', 'Supervisor'),
        ('student', 'Student'),
        ('admin', 'Administrator'),
    ]
    
    evaluation = models.ForeignKey(
        'evaluations.Evaluation',
        on_delete=models.CASCADE,
        related_name='signatures'
    )
    signer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='signatures'
    )
    signer_type = models.CharField(max_length=20, choices=SIGNER_TYPES)
    
    signature_data = models.TextField(help_text="Base64-encoded PNG signature image")
    
    signed_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['evaluation', 'signer_type']
        ordering = ['-signed_at']
    
    def __str__(self):
        return f"{self.get_signer_type_display()} signature for evaluation #{self.evaluation_id}"
    
    @property
    def is_valid(self):
        """Check if signature data exists and is not empty."""
        return bool(self.signature_data and len(self.signature_data) > 100)
