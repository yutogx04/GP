from django.core.management.base import BaseCommand
from hospitals.models import Hospital
from departments.models import Department


class Command(BaseCommand):
    help = 'Create sample hospitals and departments'

    def handle(self, *args, **options):
        hospitals_data = [
            {
                'name': 'CHU Mustapha Pacha',
                'hospital_type': 'chu',
                'address': 'Place du 1er Mai, Sidi M\'hamed',
                'city': 'Alger',
                'state': 'Alger',
                'phone': '021 23 45 67',
                'email': 'contact@chumustapha.dz',
                'total_capacity': 100,
            },
            {
                'name': 'CHU Bab El Oued',
                'hospital_type': 'chu',
                'address': 'Bd Said Touati',
                'city': 'Alger',
                'state': 'Alger',
                'phone': '021 34 56 78',
                'email': 'contact@chubeo.dz',
                'total_capacity': 80,
            },
            {
                'name': 'EPH Kouba',
                'hospital_type': 'eph',
                'address': 'Rue Mohamed Belouizdad',
                'city': 'Alger',
                'state': 'Alger',
                'phone': '021 56 78 90',
                'email': 'contact@ephkouba.dz',
                'total_capacity': 50,
            },
            {
                'name': 'Clinique El Azhar',
                'hospital_type': 'clinic',
                'address': 'Rue Didouche Mourad',
                'city': 'Alger',
                'state': 'Alger',
                'phone': '021 67 89 01',
                'email': 'contact@elazhar.dz',
                'total_capacity': 30,
            },
            {
                'name': 'Cabinet Medical Central',
                'hospital_type': 'office',
                'address': 'Rue Ben M\'hidi',
                'city': 'Alger',
                'state': 'Alger',
                'phone': '021 12 34 56',
                'email': 'contact@cabinet-central.dz',
                'total_capacity': 10,
            },
        ]

        created_hospitals = []
        for data in hospitals_data:
            hospital, created = Hospital.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            created_hospitals.append(hospital)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created hospital: {hospital.name}'))
            else:
                self.stdout.write(f'Hospital already exists: {hospital.name}')

        departments_data = [
            {'name': 'Cardiologie', 'specialty': 'Cardiology', 'capacity': 10},
            {'name': 'Neurologie', 'specialty': 'Neurology', 'capacity': 8},
            {'name': 'Pédiatrie', 'specialty': 'Pediatrics', 'capacity': 12},
            {'name': 'Chirurgie Générale', 'specialty': 'General Surgery', 'capacity': 6},
            {'name': 'Médecine Interne', 'specialty': 'Internal Medicine', 'capacity': 15},
            {'name': 'Urgences', 'specialty': 'Emergency Medicine', 'capacity': 20},
            {'name': 'Radiologie', 'specialty': 'Radiology', 'capacity': 5},
            {'name': 'Gynécologie-Obstétrique', 'specialty': 'OB-GYN', 'capacity': 8},
        ]

        for hospital in created_hospitals:
            for dept_data in departments_data:
                dept, created = Department.objects.get_or_create(
                    hospital=hospital,
                    name=dept_data['name'],
                    defaults={
                        'specialty': dept_data['specialty'],
                        'capacity': dept_data['capacity'],
                        'description': f"{dept_data['name']} department at {hospital.name}",
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  Created department: {dept.name} at {hospital.name}'))

        self.stdout.write(self.style.SUCCESS('\nSample data created successfully!'))
        self.stdout.write(f'Total hospitals: {Hospital.objects.count()}')
        self.stdout.write(f'Total departments: {Department.objects.count()}')
