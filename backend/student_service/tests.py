from django.test import TestCase
from .models import Student
from user_profile_service.models import Doyen


class StudentTest(TestCase):
    def test_student_creation(self):
        d = Doyen.objects.create(name='Dean', prenom='A')
        s = Student.objects.create(name='S', prenom='P', date_of_birth='2000-01-01', place_of_birth='PB', address='Addr', telephone='123', email='s@example.com', date_of_enrollment='2020-09-01', actif_status=True, doyen=d)
        self.assertIn('s@example.com', str(s))
