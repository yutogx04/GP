"""
Configurable evaluation form templates.
Allows administrators to define custom evaluation criteria.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class FormTemplate(models.Model):
    """Defines a reusable evaluation form template."""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_form_templates'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return self.name
    
    def get_fields_by_section(self):
        """Group fields by section for rendering."""
        sections = {}
        for field in self.fields.all().order_by('order'):
            section = field.section or 'General'
            if section not in sections:
                sections[section] = []
            sections[section].append(field)
        return sections


class FormField(models.Model):
    """Individual field in a form template."""
    
    FIELD_TYPES = [
        ('number', 'Number (0-20 scale)'),
        ('rating', 'Star Rating (1-5)'),
        ('text', 'Text (short)'),
        ('textarea', 'Text (long)'),
        ('checkbox', 'Checkbox'),
        ('select', 'Select/Dropdown'),
    ]
    
    template = models.ForeignKey(
        FormTemplate,
        on_delete=models.CASCADE,
        related_name='fields'
    )
    
    name = models.CharField(max_length=100, help_text="Internal field name")
    label = models.CharField(max_length=255, help_text="Display label")
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    
    section = models.CharField(max_length=100, blank=True, help_text="Group fields into sections")
    order = models.PositiveIntegerField(default=0)
    
    is_required = models.BooleanField(default=True)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    
    options = models.JSONField(default=list, blank=True, help_text='["Option 1", "Option 2"]')
    
    placeholder = models.CharField(max_length=255, blank=True)
    help_text = models.TextField(blank=True)
    
    weight = models.FloatField(default=1.0, help_text="Weight for grade calculation")
    
    class Meta:
        ordering = ['section', 'order']
        unique_together = ['template', 'name']
    
    def __str__(self):
        return f"{self.template.name} - {self.label}"


class FormResponse(models.Model):
    """Stores responses to a form template for an evaluation."""
    
    evaluation = models.ForeignKey(
        'evaluations.Evaluation',
        on_delete=models.CASCADE,
        related_name='form_responses'
    )
    template = models.ForeignKey(
        FormTemplate,
        on_delete=models.SET_NULL,
        null=True
    )
    
    responses = models.JSONField(default=dict)
    
    calculated_grade = models.FloatField(null=True, blank=True)
    
    submitted_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['evaluation', 'template']
    
    def calculate_grade(self):
        """Calculate weighted grade from number/rating fields."""
        total_weight = 0
        weighted_sum = 0
        
        for field in self.template.fields.filter(field_type__in=['number', 'rating']):
            value = self.responses.get(field.name)
            if value is not None:
                weighted_sum += float(value) * field.weight
                total_weight += field.weight
        
        if total_weight > 0:
            self.calculated_grade = weighted_sum / total_weight
            return self.calculated_grade
        return None
