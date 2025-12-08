
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_application_availability_notes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['-applied_at']},
        ),
        migrations.RemoveField(
            model_name='application',
            name='admin_comments',
        ),
        migrations.RemoveField(
            model_name='application',
            name='application_date',
        ),
        migrations.RemoveField(
            model_name='application',
            name='application_score',
        ),
        migrations.RemoveField(
            model_name='application',
            name='assignment_score',
        ),
        migrations.RemoveField(
            model_name='application',
            name='availability_notes',
        ),
        migrations.RemoveField(
            model_name='application',
            name='cover_letter',
        ),
        migrations.RemoveField(
            model_name='application',
            name='cv',
        ),
        migrations.RemoveField(
            model_name='application',
            name='interview_date',
        ),
        migrations.RemoveField(
            model_name='application',
            name='interview_location',
        ),
        migrations.RemoveField(
            model_name='application',
            name='interview_notes',
        ),
        migrations.RemoveField(
            model_name='application',
            name='other_documents',
        ),
        migrations.RemoveField(
            model_name='application',
            name='preferences',
        ),
        migrations.RemoveField(
            model_name='application',
            name='rejection_reason',
        ),
        migrations.RemoveField(
            model_name='application',
            name='status_update_date',
        ),
        migrations.RemoveField(
            model_name='application',
            name='supporting_documents',
        ),
        migrations.RemoveField(
            model_name='application',
            name='transcript',
        ),
        migrations.AddField(
            model_name='application',
            name='admin_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='application',
            name='applied_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='application',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='application',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='motivation_letter',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='priority',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'First Choice'), (2, 'Second Choice'), (3, 'Third Choice')], null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('reviewing', 'Under Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='application',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ApplicationDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='application_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='applications.application')),
            ],
        ),
    ]
