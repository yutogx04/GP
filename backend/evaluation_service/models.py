from django.db import models


class Evaluation(models.Model):
    evaluation_date = models.DateField(auto_now_add=True)
    evalyation = models.CharField(max_length=50)
    doctor = models.ForeignKey('establishment_service.Doctor', on_delete=models.RESTRICT)

    def __str__(self):
        return f"Evaluation {self.id} - {self.evalyation} by {self.doctor}"
