from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # 'auth_service.User'

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    numero_etudiant = models.CharField(max_length=50, blank=True)
    niveau_etude = models.CharField(max_length=50, blank=True)
    date_inscription = models.DateField(null=True, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    # other fields from ERD...
    def __str__(self):
        return f"StudentProfile({self.user.email})"

def upload_to_student(instance, filename):
    return f"students/{instance.student.user.id}/justificatives/{filename}"

class PieceJustificative(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="pieces")
    type_piece = models.CharField(max_length=100)
    nom_fichier = models.CharField(max_length=255)
    fichier = models.FileField(upload_to=upload_to_student)
    date_depot = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_piece} - {self.nom_fichier}"

class EncadrantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="encadrant_profile")
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    # other fields from ERD...
    def __str__(self):
        return f"EncadrantProfile({self.user.email})"