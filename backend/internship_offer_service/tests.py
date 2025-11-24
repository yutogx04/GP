from django.test import TestCase
from .models import Internship_announcement
from user_profile_service.models import Doyen
from establishment_service.models import Establishment, Hospital_service


class AnnouncementTest(TestCase):
    def test_announcement_creation(self):
        d = Doyen.objects.create(name='Dean', prenom='A')
        e = Establishment.objects.create(name='E', address='a', city='c', telephone='t', email='e2@example.com', doyen=d)
        s = Hospital_service.objects.create(name='S', description='desc', capacity=5, establishment=e)
        ann = Internship_announcement.objects.create(title='Intern', description='desc', start_date='2025-01-01', end_date='2025-06-01', number_of_positions=2, status='open', doyen=d, establishment=e, service=s)
        self.assertIn('Intern', str(ann))
