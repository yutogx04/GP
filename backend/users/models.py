from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

class StudentProfile(models.Model):
    NIVEAU_ETUDE_CHOICES = [
        ('l1', 'Licence 1st year'),
        ('l2', 'Licence 2nd year'),
        ('l3', 'Licence 3rd year'),
        ('m1', 'Master 1st year'),
        ('m2', 'Master 2nd year'),
        ('dc1', 'Doctorate 1st year'),
        ('dc2', 'Doctorate 2nd year'),
        ('dc3', 'Doctorate 3rd year'),
        ('intern', 'Intern'),
    ]
    
    SPECIALITE_CHOICES = [
        ('general_medicine', 'General Medicine'),
        ('surgery', 'Surgery'),
        ('pediatrics', 'Pediatrics'),
        ('gynecology', 'Gynecology-Obstetrics'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('anesthesiology', 'Anesthesiology-Resuscitation'),
        ('emergency', 'Emergency Medicine'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    student_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            MinLengthValidator(12),
            MaxLengthValidator(12),
            RegexValidator(r'^\d{12}$', 'Student number must be exactly 12 digits.')
        ]
    )
    niveau_etude = models.CharField(max_length=50, choices=NIVEAU_ETUDE_CHOICES)
    specialite = models.CharField(max_length=100, choices=SPECIALITE_CHOICES)
    faculty = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    
    average_grade = models.FloatField(null=True, blank=True)
    academic_year = models.CharField(max_length=9, default='2023-2024')
   
    registration_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    profile_completed = models.BooleanField(default=False)
    
    preferred_cities = models.JSONField(default=list, blank=True)
    preferred_specialties = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.user.full_name} - {self.student_number}"
    
    def get_age(self):
        if self.birth_date:
            today = timezone.now().date()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None
    
    def completed_internships(self):
        return self.internships.filter(status='completed').count()
    
    def average_evaluations(self):
        from evaluations.models import Evaluation
        evaluations = Evaluation.objects.filter(internship__student=self)
        if evaluations.exists():
            return sum(eval.final_grade for eval in evaluations) / evaluations.count()
        return None


class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('id_card', 'National ID Card'),
        ('birth_certificate', 'Birth Certificate'),
        ('school_certificate', 'School Certificate'),
        ('transcript', 'Academic Transcript'),
        ('insurance', 'Insurance Certificate'),
        ('medical_certificate', 'Medical Certificate'),
        ('photo', 'ID Photo'),
        ('cv', 'Curriculum Vitae'),
        ('other', 'Other'),
    ]
    
    student_profile = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='student_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    validation_date = models.DateTimeField(null=True, blank=True)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return f"{self.student_profile.user.full_name} - {self.get_document_type_display()}"


class AcademicHistory(models.Model):
    student_profile = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='academic_history'
    )
    academic_year = models.CharField(max_length=9)
    level = models.CharField(max_length=50)
    annual_average = models.FloatField()
    mention = models.CharField(max_length=50, blank=True)
    credits_obtained = models.PositiveIntegerField(default=0)
    total_credits = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-academic_year']


class Conversation(models.Model):
    """Conversation between users for messaging"""
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    subject = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation {self.id}: {self.subject or 'No subject'}"
    
    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()
    
    def unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    """Message in a conversation"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"
