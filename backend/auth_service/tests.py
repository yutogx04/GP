from django.test import TestCase
from django.contrib.auth.models import User


class UserTest(TestCase):
    def test_user_creation(self):
        u = User.objects.create_user(username='tester', email='t@example.com', password='pass')
        self.assertEqual(u.username, 'tester')
