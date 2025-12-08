
import applications.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='availability_notes',
            field=models.TextField(blank=True, help_text='Availability information'),
        ),
        migrations.AddField(
            model_name='application',
            name='cover_letter',
            field=models.FileField(blank=True, help_text='Upload your cover letter (PDF, DOC, DOCX - Max 5MB)', null=True, upload_to='application_cover_letters/', validators=[applications.validators.validate_file_size, applications.validators.validate_document_extension]),
        ),
        migrations.AddField(
            model_name='application',
            name='preferences',
            field=models.TextField(blank=True, help_text='Any specific preferences or constraints'),
        ),
        migrations.AddField(
            model_name='application',
            name='supporting_documents',
            field=models.JSONField(blank=True, default=list, help_text='Additional supporting documents (stored as file paths)'),
        ),
        migrations.AlterField(
            model_name='application',
            name='cv',
            field=models.FileField(blank=True, help_text='Upload your CV (PDF, DOC, DOCX - Max 5MB)', null=True, upload_to='application_cvs/', validators=[applications.validators.validate_file_size, applications.validators.validate_document_extension]),
        ),
    ]
