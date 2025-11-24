from django.test import TestCase
from backend.backend.models import Doyen
from backend.backend.models import Establishment, Hospital_service
from backend.backend.models import Student
from backend.backend.models import Internship_announcement
from backend.backend.models import candidacy


class CandidacyTest(TestCase):
    def test_candidacy_creation(self):
        d = Doyen.objects.create(name='Dean', prenom='A')
        e = Establishment.objects.create(name='E', address='a', city='c', telephone='t', email='e4@example.com', doyen=d)
        s = Hospital_service.objects.create(name='S', description='desc', capacity=5, establishment=e)
        stu = Student.objects.create(name='Stu', prenom='U', date_of_birth='2000-01-01', place_of_birth='PB', address='Addr', telephone='123', email='stu2@example.com', date_of_enrollment='2020-09-01', actif_status=True, doyen=d)
        ann = Internship_announcement.objects.create(title='Ann', description='desc', start_date='2025-01-01', end_date='2025-06-01', number_of_positions=1, status='open', doyen=d, establishment=e, service=s)
        c = candidacy.objects.create(status='pending', student=stu, internship_announcement=ann)
        self.assertIn('pending', str(c))
