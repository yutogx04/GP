"""
Supervisor availability management.
Allows supervisors to set recurring availability slots.
"""
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class AvailabilitySlot(models.Model):
    """Recurring availability slot for supervisors."""
    
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    SLOT_TYPES = [
        ('supervision', 'Student Supervision'),
        ('meeting', 'Meetings'),
        ('evaluation', 'Evaluations'),
        ('orientation', 'Orientation Sessions'),
        ('other', 'Other'),
    ]
    
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availability_slots'
    )
    
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    slot_type = models.CharField(max_length=20, choices=SLOT_TYPES, default='supervision')
    max_students = models.PositiveIntegerField(default=1, help_text="Max students for this slot")
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.supervisor.full_name} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
        
        overlapping = AvailabilitySlot.objects.filter(
            supervisor=self.supervisor,
            day_of_week=self.day_of_week,
            is_active=True
        ).exclude(pk=self.pk)
        
        for slot in overlapping:
            if (self.start_time < slot.end_time and self.end_time > slot.start_time):
                raise ValidationError("This slot overlaps with an existing availability slot")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class UnavailableDate(models.Model):
    """Specific dates when supervisor is unavailable (vacation, sick, etc.)."""
    
    REASON_TYPES = [
        ('vacation', 'Vacation'),
        ('sick', 'Sick Leave'),
        ('conference', 'Conference/Training'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]
    
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='unavailable_dates'
    )
    
    date = models.DateField()
    reason = models.CharField(max_length=20, choices=REASON_TYPES, default='other')
    notes = models.TextField(blank=True)
    
    all_day = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['date']
        unique_together = ['supervisor', 'date', 'start_time']
    
    def __str__(self):
        return f"{self.supervisor.full_name} - {self.date} ({self.get_reason_display()})"
