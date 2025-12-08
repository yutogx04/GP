
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='student_number',
            field=models.CharField(help_text='Enter your 12-digit student number', max_length=12, unique=True, validators=[django.core.validators.MinLengthValidator(12), django.core.validators.RegexValidator('^\\d{12}$', 'Student number must be exactly 12 digits')]),
        ),
    ]
