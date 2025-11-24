from django.test import TestCase
from backend.backend.models import Establishment, Hospital_service, Doctor
from backend.backend.models import Doyen


class EstablishmentModelsTest(TestCase):
    def test_create_establishment_and_service_and_doctor(self):
        d = Doyen.objects.create(name='Dean', prenom='A')
        e = Establishment.objects.create(name='Hosp', address='Addr', city='City', telephone='123', email='a@example.com', doyen=d)
        s = Hospital_service.objects.create(name='Cardio', description='Desc', capacity=10, establishment=e)
        doc = Doctor.objects.create(name='Doc', prenom='X', specialty='Cardio', telephone='123', email='doc@example.com', is_service_head=True, service=s)
        self.assertIn('Hosp', str(e))
        self.assertIn('Cardio', str(s))
        self.assertIn('Doc', str(doc))
