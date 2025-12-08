
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('hospital_type', models.CharField(choices=[('chu', 'CHU (University Hospital Center)'), ('eph', 'Public Health Establishment'), ('clinic', 'Private Clinic'), ('office', 'Medical Office')], max_length=50)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('total_capacity', models.PositiveIntegerField(default=0)),
                ('current_capacity', models.PositiveIntegerField(default=0)),
                ('director', models.CharField(blank=True, max_length=255)),
                ('registration_number', models.CharField(blank=True, max_length=100)),
                ('establishment_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Hospitals',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HospitalAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('appointment_date', models.DateField(auto_now_add=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admins', to='hospitals.hospital')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Hospital Administrators',
            },
        ),
    ]
