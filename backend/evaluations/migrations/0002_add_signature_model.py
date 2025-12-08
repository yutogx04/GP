
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signer_type', models.CharField(choices=[('supervisor', 'Supervisor'), ('student', 'Student'), ('admin', 'Administrator')], max_length=20)),
                ('signature_data', models.TextField(help_text='Base64-encoded PNG signature image')),
                ('signed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signatures', to='evaluations.evaluation')),
                ('signer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signatures', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-signed_at'],
                'unique_together': {('evaluation', 'signer_type')},
            },
        ),
    ]
