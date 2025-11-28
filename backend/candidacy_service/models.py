from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class CandidacyStatus(models.TextChoices):
    APPLIED = "applied", "Applied"
    SHORTLISTED = "shortlisted", "Shortlisted"
    ASSIGNED = "assigned", "Assigned"
    REJECTED = "rejected", "Rejected"

def upload_to_candidacy(instance, filename):
    return f"candidacies/{instance.student.id}/{filename}"

class Candidacy(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="candidacies")
    offer = models.ForeignKey("internship_offer_service.Offer", on_delete=models.CASCADE, related_name="candidacies")
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, choices=CandidacyStatus.choices, default=CandidacyStatus.APPLIED)
    motive_rejection = models.TextField(blank=True)
    attachment = models.FileField(upload_to=upload_to_candidacy, blank=True, null=True)  # CV / justificative snapshot
    # store some snapshot fields (optional)
    student_snapshot = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ("student", "offer")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"Candidacy(student={self.student}, offer={self.offer_id}, status={self.status})"
    def save(self, *args, **kwargs):
        # On first save, capture student snapshot
        if not self.pk:
            self.student_snapshot = {
                "email": self.student.email,
                "first_name": self.student.first_name,
                "last_name": self.student.last_name,
                "role": self.student.role,
                "is_profile_complete": self.student.is_profile_complete,
            }
        super().save(*args, **kwargs)