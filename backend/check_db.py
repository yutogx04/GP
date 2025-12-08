import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from internships.models import InternshipOffer
from authentification.models import User

print("=== INTERNSHIP OFFERS ===")
offers = InternshipOffer.objects.all()
print(f"Total offers: {offers.count()}")
for o in offers:
    print(f"  ID:{o.id}, Title:{o.title}, Created_by_id:{o.created_by_id}, Status:{o.status}, Validation:{o.validation_status}")

print("\n=== HOSPITAL ADMIN USERS ===")
hospital_admins = User.objects.filter(role='hospital_admin')
for u in hospital_admins:
    print(f"  ID:{u.id}, Email:{u.email}")
