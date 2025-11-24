from django.db import models


class Internship_announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_positions = models.IntegerField()
    publication_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    doyen = models.ForeignKey('user_profile_service.Doyen', on_delete=models.RESTRICT)
    establishment = models.ForeignKey('establishment_service.Establishment', on_delete=models.RESTRICT)
    service = models.ForeignKey('establishment_service.Hospital_service', on_delete=models.RESTRICT)

    def __str__(self):
        return f"Announcement: {self.title} ({self.status})"
