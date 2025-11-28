from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Evaluation(models.Model):
    stage = models.ForeignKey("internship_service.Stage", on_delete=models.CASCADE, related_name="evaluations")
    medecin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="evaluations_done")
    note_competences = models.PositiveSmallIntegerField()
    note_assiduite = models.PositiveSmallIntegerField()
    note_comportement = models.PositiveSmallIntegerField()
    commentaire = models.TextField(blank=True)
    date_evaluation = models.DateTimeField(auto_now_add=True)
    pdf_report = models.FileField(upload_to="evaluations/reports/", blank=True, null=True)

    def __str__(self):
        return f"Evaluation(stage={self.stage_id}, by={self.medecin})"
    
class EvaluationCriteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name