from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class InternshipStatus(models.TextChoices):
    ONGOING = "ongoing", "Ongoing"
    FINISHED = "finished", "Finished"
    CANCELLED = "cancelled", "Cancelled"

class Stage(models.Model):
    # Stage corresponds to ERD Stage: the actual assigned internship
    candidacy = models.OneToOneField("candidacy_service.Candidacy", on_delete=models.CASCADE, related_name="stage")
    medecin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="supervised_stages")  # encadrant
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=30, choices=InternshipStatus.choices, default=InternshipStatus.ONGOING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # optional final report file
    final_report = models.FileField(upload_to="stages/reports/", blank=True, null=True)

    def mark_finished(self):
        self.status = InternshipStatus.FINISHED
        self.save(update_fields=["status", "updated_at"])
    
    def mark_cancelled(self):
        self.status = InternshipStatus.CANCELLED
        self.save(update_fields=["status", "updated_at"])