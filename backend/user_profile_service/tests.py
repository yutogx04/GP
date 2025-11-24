from django.test import TestCase
from .models import Doyen


class DoyenModelTest(TestCase):
    def test_create_doyen(self):
        d = Doyen.objects.create(name='John', prenom='Doe')
        self.assertEqual(str(d), 'Doyen: John Doe')
