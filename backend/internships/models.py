from django.db import models
from django.conf import settings
from django.utils import timezone


class InternshipOffer(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    
    VALIDATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    TYPE_CHOICES = [
        ('clinical', 'Clinical'),
        ('research', 'Research'),
        ('observation', 'Observation'),
    ]
    
    LEVEL_CHOICES = [
        ('l1', 'Licence 1'),
        ('l2', 'Licence 2'),
        ('l3', 'Licence 3'),
        ('m1', 'Master 1'),
        ('m2', 'Master 2'),
        ('any', 'All Levels'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    prerequisites = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    
    hospital = models.ForeignKey(
        'hospitals.Hospital',
        on_delete=models.CASCADE,
        related_name='internship_offers'
    )
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='internship_offers'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_offers'
    )
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='clinical')
    minimum_study_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='l3')
    
    start_date = models.DateField()
    end_date = models.DateField()
    application_deadline = models.DateField()
    
    slots = models.PositiveIntegerField(default=1)
    available_slots = models.PositiveIntegerField(default=1)
    
    is_paid = models.BooleanField(default=False)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    required_skills = models.JSONField(default=list, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    validation_status = models.CharField(max_length=20, choices=VALIDATION_STATUS_CHOICES, default='pending')
    
    is_urgent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.hospital.name}"
    
    @property
    def hospital_name(self):
        return self.hospital.name
    
    @property
    def department_name(self):
        return self.department.name
    
    @property
    def type_display(self):
        return dict(self.TYPE_CHOICES).get(self.type, self.type)
    
    @property
    def minimum_study_level_display(self):
        return dict(self.LEVEL_CHOICES).get(self.minimum_study_level, self.minimum_study_level)
    
    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class Internship(models.Model):
    """Confirmed internship placement for a student"""
    STATUS_CHOICES = [
        ('pending', 'Pending Start'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    offer = models.ForeignKey(
        InternshipOffer,
        on_delete=models.CASCADE,
        related_name='placements'
    )
    student = models.ForeignKey(
        'users.StudentProfile',
        on_delete=models.CASCADE,
        related_name='internships'
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_internships'
    )
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    assigned_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-assigned_at']
        unique_together = ['offer', 'student']
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.offer.title}"


class InternshipJournal(models.Model):
    """Daily journal entries for internship"""
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='journal_entries'
    )
    date = models.DateField(default=timezone.now)
    activities = models.TextField(default='')
    skills_practiced = models.JSONField(default=list, blank=True)
    challenges = models.TextField(blank=True)
    supervisor_comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['internship', 'date']
    
    def __str__(self):
        return f"{self.internship.student.user.full_name} - {self.date}"


class Schedule(models.Model):
    """Calendar events for internships"""
    EVENT_TYPE_CHOICES = [
        ('shift', 'Shift'),
        ('meeting', 'Meeting'),
        ('training', 'Training'),
        ('evaluation', 'Evaluation'),
        ('orientation', 'Orientation'),
        ('other', 'Other'),
    ]
    
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='schedules',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='shift')
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    location = models.CharField(max_length=255, blank=True)
    
    reminder_24h = models.BooleanField(default=True)
    reminder_1h = models.BooleanField(default=True)
    reminder_sent_24h = models.BooleanField(default=False)
    reminder_sent_1h = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"

