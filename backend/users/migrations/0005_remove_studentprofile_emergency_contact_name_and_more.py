
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_studentprofile_emergency_contact_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='emergency_contact_name',
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='emergency_phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
