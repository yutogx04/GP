import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from applications.models import Application
from authentification.models import User

print("=== APPLICATIONS ===")
apps = Application.objects.all()
print(f"Total applications: {apps.count()}")
for app in apps:
    print(f"  ID:{app.id}, Student:{app.student.email if app.student else 'N/A'}, Offer:{app.offer.title if app.offer else 'N/A'}, Status:{app.status}")

print("\n=== STUDENTS ===")
students = User.objects.filter(role='student')
for s in students:
    print(f"  ID:{s.id}, Email:{s.email}")
