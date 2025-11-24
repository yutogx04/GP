from django.db import models


class Doyen(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)


class Establishment(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    doyen = models.ForeignKey(Doyen, on_delete=models.RESTRICT)


class Hospital_service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    capacity = models.IntegerField()
    establishment = models.ForeignKey(Establishment, on_delete=models.RESTRICT)


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    # TO-DO: fix
    is_service_head = models.BooleanField(default=False)
    service = models.ForeignKey(Hospital_service, on_delete=models.RESTRICT)


class Evaluation(models.Model):
    evaluation_date = models.DateField(auto_now_add=True)
    evalyation = models.CharField(max_length=50)
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT)


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
    doyen = models.ForeignKey(Doyen, on_delete=models.RESTRICT)
    evaluations = models.ManyToManyField(Evaluation)


class Document(models.Model):
    title = models.CharField(max_length=200)
    path = models.FileField(upload_to="documents/")
    upload_date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)


class Internship_announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_positions = models.IntegerField()
    publication_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    doyen = models.ForeignKey(Doyen, on_delete=models.RESTRICT)
    establishment = models.ForeignKey(Establishment, on_delete=models.RESTRICT)
    service = models.ForeignKey(Hospital_service, on_delete=models.RESTRICT)


class Internship(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    doyen = models.ForeignKey(Doyen, on_delete=models.RESTRICT)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT)


class Candidacy(models.Model):
    date_of_application = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    reason_of_refusal = models.TextField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    internship_announcement = models.ForeignKey(
        Internship_announcement, on_delete=models.RESTRICT
    )
    internship = models.OneToOneField(
        Internship, on_delete=models.RESTRICT, null=True, blank=True
    )
