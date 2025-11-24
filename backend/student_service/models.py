from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_of_enrollment = models.DateField()
    actif_status = models.BooleanField(default=True)
    doyen = models.ForeignKey('user_profile_service.Doyen', on_delete=models.RESTRICT)
    evaluations = models.ManyToManyField('evaluation_service.Evaluation')

    def __str__(self):
        return f"Student: {self.name} {self.prenom} ({self.email})"
