from django.db import models


class Internship(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    doyen = models.ForeignKey('user_profile_service.Doyen', on_delete=models.RESTRICT)
    student = models.ForeignKey('student_service.Student', on_delete=models.RESTRICT)
    doctor = models.ForeignKey('establishment_service.Doctor', on_delete=models.RESTRICT)

    def __str__(self):
        return f"Internship {self.id} - {self.student} with {self.doctor} ({self.status})"
