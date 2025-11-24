from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=200)
    path = models.FileField(upload_to="documents/")
    upload_date = models.DateField(auto_now_add=True)
    student = models.ForeignKey('student_service.Student', on_delete=models.RESTRICT)

    def __str__(self):
        return f"Document: {self.title} (student={self.student})"
