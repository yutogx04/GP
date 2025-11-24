from django.test import TestCase
from backend.models import Doyen
from backend.models import Establishment, Hospital_service, Doctor
from backend.models import Student
from backend.models import Internship


class InternshipTest(TestCase):
    def test_internship_creation(self):
        d = Doyen.objects.create(name='Dean', prenom='A')
        e = Establishment.objects.create(name='E', address='a', city='c', telephone='t', email='e3@example.com', doyen=d)
        s = Hospital_service.objects.create(name='S', description='desc', capacity=5, establishment=e)
        doc = Doctor.objects.create(name='Doc', prenom='P', specialty='X', telephone='t', email='doc2@example.com', is_service_head=False, service=s)
        stu = Student.objects.create(name='Stu', prenom='U', date_of_birth='2000-01-01', place_of_birth='PB', address='Addr', telephone='123', email='stu@example.com', date_of_enrollment='2020-09-01', actif_status=True, doyen=d)
        it = Internship.objects.create(start_date='2025-01-01', end_date='2025-06-01', status='active', doyen=d, student=stu, doctor=doc)
        self.assertIn('active', str(it))
