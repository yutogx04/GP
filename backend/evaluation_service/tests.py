from django.test import TestCase
from backend.backend.models import Doctor, Hospital_service, Establishment
from backend.backend.models import Doyen
from backend.backend.models import Evaluation


class EvaluationTest(TestCase):
    def test_evaluation_creation(self):
        d = Doyen.objects.create(name='Dean', prenom='A')
        e = Establishment.objects.create(name='E', address='a', city='c', telephone='t', email='e@example.com', doyen=d)
        s = Hospital_service.objects.create(name='S', description='desc', capacity=5, establishment=e)
        doc = Doctor.objects.create(name='Doc', prenom='P', specialty='X', telephone='t', email='doc@example.com', is_service_head=False, service=s)
        ev = Evaluation.objects.create(evalyation='Good', doctor=doc)
        self.assertIn('Good', str(ev))
