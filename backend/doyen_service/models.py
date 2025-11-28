from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class AssignmentOverride(models.Model):
    # records manual overrides performed by doyens/faculty admins
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="overrides_made")
    candidacy_id = models.IntegerField()  # store candidacy id for audit
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        app_label = 'doyen_service'

    def __str__(self):
        return f"Override by {self.performed_by} on candidacy {self.candidacy_id}"
    
class DoyenProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doyen_profile")
    faculty_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=30, blank=True)
    office_address = models.TextField(blank=True)

    def __str__(self):
        return f"DoyenProfile({self.user.email})"