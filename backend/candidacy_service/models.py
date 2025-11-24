from django.db import models


class candidacy(models.Model):
    date_of_application = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    reason_of_refusal = models.TextField(null=True, blank=True)
    student = models.ForeignKey('student_service.Student', on_delete=models.RESTRICT)
    internship_announcement = models.ForeignKey('internship_offer_service.Internship_announcement', on_delete=models.RESTRICT)
    internship = models.OneToOneField('internship_service.Internship', on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return f"Candidacy {self.id} - {self.status} for {self.student}"
