
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_alter_application_options_and_more'),
        ('evaluations', '0002_add_signature_model'),
        ('notifications', '0001_initial'),
        ('users', '0007_availabilityslot_unavailabledate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.CharField(choices=[('email', 'Email'), ('in_app', 'In-App Notification'), ('message', 'Direct Message'), ('sms', 'SMS'), ('push', 'Push Notification')], max_length=20)),
                ('direction', models.CharField(choices=[('outbound', 'Outbound (System to User)'), ('inbound', 'Inbound (User to System)'), ('internal', 'Internal (User to User)')], default='outbound', max_length=20)),
                ('recipient_email', models.EmailField(blank=True, help_text='For external recipients', max_length=254)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('content_preview', models.TextField(blank=True, help_text='First 500 chars', max_length=500)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('read', 'Read'), ('failed', 'Failed'), ('bounced', 'Bounced')], default='pending', max_length=20)),
                ('error_message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('template_used', models.CharField(blank=True, max_length=100)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_communications', to=settings.AUTH_USER_MODEL)),
                ('related_application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='applications.application')),
                ('related_evaluation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='evaluations.evaluation')),
                ('related_message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.message')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_communications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['channel', 'status'], name='notificatio_channel_6229c8_idx'), models.Index(fields=['recipient', 'created_at'], name='notificatio_recipie_3aa0f8_idx'), models.Index(fields=['sender', 'created_at'], name='notificatio_sender__ab15c7_idx')],
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('template_type', models.CharField(choices=[('verification', 'Email Verification'), ('password_reset', 'Password Reset'), ('application_status', 'Application Status Update'), ('reminder', 'Reminder Notification'), ('evaluation_ready', 'Evaluation Ready'), ('welcome', 'Welcome Email'), ('assignment_notification', 'Assignment Notification'), ('custom', 'Custom Template')], max_length=50)),
                ('subject', models.CharField(help_text='Use {{ variable }} for dynamic content', max_length=255)),
                ('html_content', models.TextField(help_text='HTML template with Django template syntax')),
                ('plain_content', models.TextField(blank=True, help_text='Plain text fallback')),
                ('is_active', models.BooleanField(default=True)),
                ('is_default', models.BooleanField(default=False, help_text='Default template for this type')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('available_variables', models.JSONField(default=list, help_text='["user_name", "application_status", "link"]')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_email_templates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['template_type', 'name'],
                'unique_together': {('template_type', 'is_default')},
            },
        ),
    ]
