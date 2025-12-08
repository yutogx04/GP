
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0001_initial'),
        ('users', '0005_remove_studentprofile_emergency_contact_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='internship',
            options={'ordering': ['-assigned_at']},
        ),
        migrations.AlterModelOptions(
            name='internshipjournal',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='internshipoffer',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterUniqueTogether(
            name='internship',
            unique_together={('offer', 'student')},
        ),
        migrations.RemoveField(
            model_name='internshipoffer',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='internshipoffer',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='internshipoffer',
            name='internship_type',
        ),
        migrations.RemoveField(
            model_name='internshipoffer',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='internshipoffer',
            name='modification_date',
        ),
        migrations.RemoveField(
            model_name='internshipoffer',
            name='publication_date',
        ),
        migrations.RemoveField(
            model_name='internshipoffer',
            name='required_specialties',
        ),
        migrations.RemoveField(
            model_name='internshipoffer',
            name='views',
        ),
        migrations.AddField(
            model_name='internship',
            name='assigned_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='internshipjournal',
            name='activities',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='internshipjournal',
            name='challenges',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='internshipjournal',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='internshipjournal',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='internshipjournal',
            name='skills_practiced',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='internshipjournal',
            name='supervisor_comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='internshipjournal',
            unique_together={('internship', 'date')},
        ),
        migrations.AddField(
            model_name='internshipoffer',
            name='available_slots',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='internshipoffer',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='internshipoffer',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_offers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='internshipoffer',
            name='type',
            field=models.CharField(choices=[('clinical', 'Clinical'), ('research', 'Research'), ('observation', 'Observation')], default='clinical', max_length=20),
        ),
        migrations.AddField(
            model_name='internshipoffer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='internshipoffer',
            name='validation_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='internship',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placements', to='internships.internshipoffer'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Start'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='internship',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_internships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='internshipjournal',
            name='internship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', to='internships.internship'),
        ),
        migrations.AlterField(
            model_name='internshipoffer',
            name='benefits',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='internshipoffer',
            name='minimum_study_level',
            field=models.CharField(choices=[('l1', 'Licence 1'), ('l2', 'Licence 2'), ('l3', 'Licence 3'), ('m1', 'Master 1'), ('m2', 'Master 2'), ('any', 'All Levels')], default='l3', max_length=10),
        ),
        migrations.AlterField(
            model_name='internshipoffer',
            name='slots',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='internshipoffer',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending Approval'), ('open', 'Open'), ('closed', 'Closed')], default='draft', max_length=20),
        ),
        migrations.RemoveField(
            model_name='internship',
            name='actual_end_date',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='actual_start_date',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='application',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='assigned_tasks',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='defense_date',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='defense_location',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='department',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='journal_frequency',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='journal_required',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='learning_objectives',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='modification_date',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='target_skills',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='weekly_hours',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='activities_performed',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='activity_date',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='developed_skills',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='difficulties_encountered',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='modification_date',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='solutions_provided',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='student_signature',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='supervisor_notes',
        ),
        migrations.RemoveField(
            model_name='internshipjournal',
            name='supervisor_signature',
        ),
    ]
