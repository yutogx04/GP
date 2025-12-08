
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(max_length=50, unique=True)),
                ('niveau_etude', models.CharField(choices=[('l1', 'Licence 1st year'), ('l2', 'Licence 2nd year'), ('l3', 'Licence 3rd year'), ('m1', 'Master 1st year'), ('m2', 'Master 2nd year'), ('dc1', 'Doctorate 1st year'), ('dc2', 'Doctorate 2nd year'), ('dc3', 'Doctorate 3rd year'), ('intern', 'Intern')], max_length=50)),
                ('specialite', models.CharField(choices=[('general_medicine', 'General Medicine'), ('surgery', 'Surgery'), ('pediatrics', 'Pediatrics'), ('gynecology', 'Gynecology-Obstetrics'), ('cardiology', 'Cardiology'), ('neurology', 'Neurology'), ('psychiatry', 'Psychiatry'), ('radiology', 'Radiology'), ('anesthesiology', 'Anesthesiology-Resuscitation'), ('emergency', 'Emergency Medicine')], max_length=100)),
                ('faculty', models.CharField(max_length=255)),
                ('university', models.CharField(max_length=255)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('birth_place', models.CharField(blank=True, max_length=255)),
                ('address', models.TextField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('emergency_phone', models.CharField(blank=True, max_length=20)),
                ('average_grade', models.FloatField(blank=True, null=True)),
                ('academic_year', models.CharField(default='2023-2024', max_length=9)),
                ('registration_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('profile_completed', models.BooleanField(default=False)),
                ('preferred_cities', models.JSONField(blank=True, default=list)),
                ('preferred_specialties', models.JSONField(blank=True, default=list)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('id_card', 'National ID Card'), ('birth_certificate', 'Birth Certificate'), ('school_certificate', 'School Certificate'), ('transcript', 'Academic Transcript'), ('insurance', 'Insurance Certificate'), ('medical_certificate', 'Medical Certificate'), ('photo', 'ID Photo'), ('cv', 'Curriculum Vitae'), ('other', 'Other')], max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='student_documents/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('is_validated', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True)),
                ('validation_date', models.DateTimeField(blank=True, null=True)),
                ('validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('student_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='users.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='AcademicHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.CharField(max_length=9)),
                ('level', models.CharField(max_length=50)),
                ('annual_average', models.FloatField()),
                ('mention', models.CharField(blank=True, max_length=50)),
                ('credits_obtained', models.PositiveIntegerField(default=0)),
                ('total_credits', models.PositiveIntegerField(default=0)),
                ('student_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_history', to='users.studentprofile')),
            ],
            options={
                'ordering': ['-academic_year'],
            },
        ),
    ]
