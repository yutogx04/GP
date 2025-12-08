
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_studentprofile_student_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='emergency_contact_name',
            field=models.CharField(blank=True, help_text='Emergency contact full name', max_length=100),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='emergency_phone',
            field=models.CharField(blank=True, help_text='Emergency contact phone number', max_length=20),
        ),
    ]
