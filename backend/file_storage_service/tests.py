from django.test import TestCase
from backend.models import Student
from backend.models import Document
from backend.models import Doyen


class DocumentTest(TestCase):
    def test_document_creation(self):
        d = Doyen.objects.create(name='Dean', prenom='A')
        s = Student.objects.create(name='S', prenom='P', date_of_birth='2000-01-01', place_of_birth='PB', address='Addr', telephone='123', email='s2@example.com', date_of_enrollment='2020-09-01', actif_status=True, doyen=d)
        doc = Document.objects.create(title='Doc1', path='documents/test.txt', student=s)
        self.assertIn('Doc1', str(doc))
