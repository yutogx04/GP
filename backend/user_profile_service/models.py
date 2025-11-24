from django.db import models


class Doyen(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"Doyen: {self.name} {self.prenom}"
