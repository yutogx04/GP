from django.db import models


class Establishment(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    doyen = models.ForeignKey('user_profile_service.Doyen', on_delete=models.RESTRICT)

    def __str__(self):
        return f"Establishment: {self.name} ({self.city})"


class Hospital_service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    capacity = models.IntegerField()
    establishment = models.ForeignKey('establishment_service.Establishment', on_delete=models.RESTRICT)

    def __str__(self):
        return f"Service: {self.name} (@{self.establishment.name})"


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_service_head = models.BooleanField(default=False)
    service = models.ForeignKey('establishment_service.Hospital_service', on_delete=models.RESTRICT)

    def __str__(self):
        return f"Doctor: {self.name} {self.prenom} ({self.specialty})"
