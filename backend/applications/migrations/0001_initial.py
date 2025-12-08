
import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivation_letter', models.TextField()),
                ('cv', models.FileField(blank=True, null=True, upload_to='application_cvs/')),
                ('transcript', models.FileField(blank=True, null=True, upload_to='application_transcripts/')),
                ('other_documents', models.JSONField(blank=True, default=list)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('pre_selected', 'Pre-selected'), ('interview', 'Interview Scheduled'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='pending', max_length=50)),
                ('application_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status_update_date', models.DateTimeField(auto_now=True)),
                ('application_score', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('admin_comments', models.TextField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('interview_date', models.DateTimeField(blank=True, null=True)),
                ('interview_location', models.CharField(blank=True, max_length=255, null=True)),
                ('interview_notes', models.TextField(blank=True, null=True)),
                ('assignment_score', models.FloatField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Applications',
                'ordering': ['-application_date'],
            },
        ),
    ]
