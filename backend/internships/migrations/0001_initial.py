
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
        ('departments', '0001_initial'),
        ('hospitals', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('internship_type', models.CharField(choices=[('mandatory', 'Mandatory Internship'), ('voluntary', 'Voluntary Internship'), ('research', 'Research Internship'), ('observation', 'Observation Internship')], default='mandatory', max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('application_deadline', models.DateField()),
                ('slots', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('minimum_study_level', models.CharField(choices=[('l1', 'Licence 1st year'), ('l2', 'Licence 2nd year'), ('l3', 'Licence 3rd year'), ('m1', 'Master 1st year'), ('m2', 'Master 2nd year'), ('dc1', 'Doctorate 1st year'), ('dc2', 'Doctorate 2nd year'), ('dc3', 'Doctorate 3rd year'), ('intern', 'Intern')], max_length=50)),
                ('required_specialties', models.JSONField(blank=True, default=list)),
                ('required_skills', models.JSONField(blank=True, default=list)),
                ('prerequisites', models.TextField(blank=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('benefits', models.JSONField(blank=True, default=list)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending'), ('published', 'Published'), ('closed', 'Closed'), ('cancelled', 'Cancelled')], default='draft', max_length=50)),
                ('publication_date', models.DateTimeField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('keywords', models.JSONField(blank=True, default=list)),
                ('is_urgent', models.BooleanField(default=False)),
                ('views', models.PositiveIntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_offers', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internship_offers', to='departments.department')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internship_offers', to='hospitals.hospital')),
            ],
            options={
                'verbose_name_plural': 'Internship Offers',
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_start_date', models.DateField(blank=True, null=True)),
                ('actual_end_date', models.DateField(blank=True, null=True)),
                ('weekly_hours', models.PositiveIntegerField(default=35)),
                ('status', models.CharField(choices=[('to_start', 'To Start'), ('in_progress', 'In Progress'), ('suspended', 'Suspended'), ('completed', 'Completed'), ('abandoned', 'Abandoned'), ('cancelled', 'Cancelled')], default='to_start', max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('learning_objectives', models.JSONField(blank=True, default=list)),
                ('assigned_tasks', models.JSONField(blank=True, default=list)),
                ('target_skills', models.JSONField(blank=True, default=list)),
                ('defense_date', models.DateField(blank=True, null=True)),
                ('defense_location', models.CharField(blank=True, max_length=255)),
                ('journal_required', models.BooleanField(default=True)),
                ('journal_frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily', max_length=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='internship', to='applications.application')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internships', to='departments.department')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internships', to='users.studentprofile')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervised_internships', to=settings.AUTH_USER_MODEL)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internships', to='internships.internshipoffer')),
            ],
            options={
                'verbose_name_plural': 'Internships',
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='InternshipJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_date', models.DateField()),
                ('activities_performed', models.TextField()),
                ('developed_skills', models.JSONField(blank=True, default=list)),
                ('difficulties_encountered', models.TextField(blank=True)),
                ('solutions_provided', models.TextField(blank=True)),
                ('supervisor_notes', models.TextField(blank=True)),
                ('student_signature', models.BooleanField(default=False)),
                ('supervisor_signature', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='internships.internship')),
            ],
            options={
                'verbose_name_plural': 'Internship Journals',
                'ordering': ['-activity_date'],
                'unique_together': {('internship', 'activity_date')},
            },
        ),
    ]
