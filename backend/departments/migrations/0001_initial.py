
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospitals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('capacity', models.PositiveIntegerField(default=5)),
                ('specialty', models.CharField(max_length=255)),
                ('internal_phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headed_departments', to=settings.AUTH_USER_MODEL)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='hospitals.hospital')),
            ],
            options={
                'verbose_name_plural': 'Departments',
                'ordering': ['name'],
            },
        ),
    ]
