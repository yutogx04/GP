from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Establishment(models.Model):
    # Minimal representation — move to establishment_service if you already have one
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class ServiceHospitalier(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    capacite_accueil = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} @ {self.establishment.name}"

class AnnouncementStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    CLOSED = "closed", "Closed"

class Offer(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name="offers")
    service = models.ForeignKey(ServiceHospitalier, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    number_places = models.PositiveIntegerField(default=1)
    date_publication = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=AnnouncementStatus.choices, default=AnnouncementStatus.DRAFT)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_offers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_publication", "-created_at"]

    def publish(self, by_user=None):
        self.status = AnnouncementStatus.PUBLISHED
        self.date_publication = timezone.now()
        if by_user:
            self.created_by = by_user
        self.save(update_fields=["status", "date_publication", "created_by"])
    def close(self):
        self.status = AnnouncementStatus.CLOSED
        self.save(update_fields=["status"])