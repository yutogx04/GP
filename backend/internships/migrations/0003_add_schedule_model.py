
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0002_alter_internship_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('event_type', models.CharField(choices=[('shift', 'Shift'), ('meeting', 'Meeting'), ('training', 'Training'), ('evaluation', 'Evaluation'), ('orientation', 'Orientation'), ('other', 'Other')], default='shift', max_length=20)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('location', models.CharField(blank=True, max_length=255)),
                ('reminder_24h', models.BooleanField(default=True)),
                ('reminder_1h', models.BooleanField(default=True)),
                ('reminder_sent_24h', models.BooleanField(default=False)),
                ('reminder_sent_1h', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('internship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='internships.internship')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date', 'start_time'],
            },
        ),
    ]
