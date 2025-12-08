
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_conversation_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilitySlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('slot_type', models.CharField(choices=[('supervision', 'Student Supervision'), ('meeting', 'Meetings'), ('evaluation', 'Evaluations'), ('orientation', 'Orientation Sessions'), ('other', 'Other')], default='supervision', max_length=20)),
                ('max_students', models.PositiveIntegerField(default=1, help_text='Max students for this slot')),
                ('location', models.CharField(blank=True, max_length=255)),
                ('notes', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_until', models.DateField(blank=True, null=True)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability_slots', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['day_of_week', 'start_time'],
            },
        ),
        migrations.CreateModel(
            name='UnavailableDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reason', models.CharField(choices=[('vacation', 'Vacation'), ('sick', 'Sick Leave'), ('conference', 'Conference/Training'), ('personal', 'Personal'), ('other', 'Other')], default='other', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('all_day', models.BooleanField(default=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unavailable_dates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
                'unique_together': {('supervisor', 'date', 'start_time')},
            },
        ),
    ]
