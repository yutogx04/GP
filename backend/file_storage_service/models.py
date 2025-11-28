from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class StoredFile(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="uploaded_files")
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    mime_type = models.CharField(max_length=255, blank=True)
    size = models.PositiveIntegerField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and not self.size:
            self.size = self.file.size
        super().save(*args, **kwargs)
    def __str__(self):
        return f"StoredFile(id={self.id}, uploader={self.uploader}, size={self.size})"