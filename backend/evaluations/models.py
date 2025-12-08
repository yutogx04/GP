from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Evaluation(models.Model):
    internship = models.OneToOneField(
        'internships.Internship', 
        on_delete=models.CASCADE, 
        related_name='evaluation'
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='supervisor_evaluations'
    )
    
    technical_skills = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    attendance_punctuality = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    patient_relation = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    teamwork = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    initiative_autonomy = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    theoretical_knowledge = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    
    final_grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    
    overall_appreciation = models.TextField(blank=True, null=True)
    strengths = models.JSONField(default=list, blank=True)
    areas_for_improvement = models.JSONField(default=list, blank=True)
    recommendations = models.TextField(blank=True, null=True)
    
    suitable_for_next_internship = models.BooleanField(null=True, blank=True)
    recommend_for_supervision = models.BooleanField(null=True, blank=True)
    thesis_opinion = models.TextField(blank=True, null=True)
    
    evaluation_date = models.DateTimeField(default=timezone.now)
    is_submitted = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    validation_date = models.DateTimeField(null=True, blank=True)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='validated_evaluations'
    )
    
    supervisor_signature = models.BooleanField(default=False)
    student_signature = models.BooleanField(default=False)
    admin_signature = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Evaluation: {self.internship.student.user.full_name} - {self.internship.offer.title}"
    
    def calculate_final_grade(self):
        """Calculate the weighted final grade"""
        if all([
            self.technical_skills, self.attendance_punctuality, self.patient_relation,
            self.teamwork, self.initiative_autonomy, self.theoretical_knowledge
        ]):
            grades = [
                self.technical_skills * 0.25,      # 25%
                self.attendance_punctuality * 0.15, # 15%
                self.patient_relation * 0.15,       # 15%
                self.teamwork * 0.15,              # 15%
                self.initiative_autonomy * 0.15,    # 15%
                self.theoretical_knowledge * 0.15   # 15%
            ]
            self.final_grade = sum(grades)
            self.save(update_fields=['final_grade'])
        return self.final_grade
    
    def get_mention(self):
        """Returns the mention based on the final grade"""
        if not self.final_grade:
            return None
        
        if self.final_grade >= 16:
            return "Very Good"
        elif self.final_grade >= 14:
            return "Good"
        elif self.final_grade >= 12:
            return "Fairly Good"
        elif self.final_grade >= 10:
            return "Passable"
        else:
            return "Insufficient"
    
    class Meta:
        ordering = ['-evaluation_date']
        verbose_name_plural = "Evaluations"

class AutoEvaluation(models.Model):
    internship = models.OneToOneField(
        'internships.Internship', 
        on_delete=models.CASCADE, 
        related_name='auto_evaluation'
    )
    
    acquired_skills_grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    supervision_satisfaction_grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    working_conditions_grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        null=True, blank=True
    )
    
    acquired_skills = models.JSONField(default=list, blank=True)
    difficulties_encountered = models.TextField(blank=True, null=True)
    positive_points = models.TextField(blank=True, null=True)
    improvement_suggestions = models.TextField(blank=True, null=True)
    professional_project = models.TextField(blank=True, null=True)
    
    submission_date = models.DateTimeField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Auto-evaluation: {self.internship.student.user.full_name}"
    
    class Meta:
        verbose_name_plural = "Auto-evaluations"