"""
Customizable email template system.
Allows administrators to create and manage email templates.
"""
from django.db import models
from django.conf import settings
from django.template import Template, Context
from django.utils import timezone


class EmailTemplate(models.Model):
    """Customizable email template for notifications."""
    
    TEMPLATE_TYPES = [
        ('verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
        ('application_status', 'Application Status Update'),
        ('reminder', 'Reminder Notification'),
        ('evaluation_ready', 'Evaluation Ready'),
        ('welcome', 'Welcome Email'),
        ('assignment_notification', 'Assignment Notification'),
        ('custom', 'Custom Template'),
    ]
    
    name = models.CharField(max_length=255)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    
    subject = models.CharField(max_length=255, help_text="Use {{ variable }} for dynamic content")
    html_content = models.TextField(help_text="HTML template with Django template syntax")
    plain_content = models.TextField(blank=True, help_text="Plain text fallback")
    
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False, help_text="Default template for this type")
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_email_templates'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    available_variables = models.JSONField(
        default=list,
        help_text='["user_name", "application_status", "link"]'
    )
    
    class Meta:
        ordering = ['template_type', 'name']
        unique_together = ['template_type', 'is_default']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def render(self, context_data):
        """Render the template with given context data."""
        subject_template = Template(self.subject)
        html_template = Template(self.html_content)
        
        context = Context(context_data)
        
        return {
            'subject': subject_template.render(context),
            'html': html_template.render(context),
            'plain': Template(self.plain_content).render(context) if self.plain_content else None
        }
    
    @classmethod
    def get_template(cls, template_type, use_default=True):
        """Get active template for a given type."""
        template = cls.objects.filter(
            template_type=template_type,
            is_active=True,
            is_default=True
        ).first()
        
        if not template and use_default:
            template = cls.objects.filter(
                template_type=template_type,
                is_active=True
            ).first()
        
        return template


DEFAULT_TEMPLATES = [
    {
        'name': 'Default Verification Email',
        'template_type': 'verification',
        'subject': 'Verify your MedIntern account',
        'html_content': '''
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #0ea5e9;">Welcome to MedIntern!</h1>
        <p>Hi {{ user_name }},</p>
        <p>Please verify your email address by clicking the button below:</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{{ verification_link }}" style="background-color: #0ea5e9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; display: inline-block;">
                Verify Email
            </a>
        </p>
        <p>If you didn't create this account, you can ignore this email.</p>
        <p>Best regards,<br>The MedIntern Team</p>
    </div>
</body>
</html>
''',
        'is_default': True,
        'available_variables': ['user_name', 'verification_link']
    },
    {
        'name': 'Default Password Reset',
        'template_type': 'password_reset',
        'subject': 'Reset your MedIntern password',
        'html_content': '''
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #0ea5e9;">Password Reset</h1>
        <p>Hi {{ user_name }},</p>
        <p>You requested to reset your password. Click the button below:</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{{ reset_link }}" style="background-color: #0ea5e9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; display: inline-block;">
                Reset Password
            </a>
        </p>
        <p>This link expires in 24 hours.</p>
        <p>If you didn't request this, ignore this email.</p>
        <p>Best regards,<br>The MedIntern Team</p>
    </div>
</body>
</html>
''',
        'is_default': True,
        'available_variables': ['user_name', 'reset_link']
    },
    {
        'name': 'Default Application Status',
        'template_type': 'application_status',
        'subject': 'Application Update: {{ offer_title }}',
        'html_content': '''
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #0ea5e9;">Application Update</h1>
        <p>Hi {{ student_name }},</p>
        <p>Your application for <strong>{{ offer_title }}</strong> at {{ hospital_name }} has been updated.</p>
        <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Status:</strong> <span style="color: {{ status_color }};">{{ status }}</span></p>
        </div>
        {% if message %}
        <p><strong>Message from reviewer:</strong></p>
        <p style="background: #f1f5f9; padding: 15px; border-radius: 6px;">{{ message }}</p>
        {% endif %}
        <p style="text-align: center; margin: 30px 0;">
            <a href="{{ application_link }}" style="background-color: #0ea5e9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; display: inline-block;">
                View Application
            </a>
        </p>
        <p>Best regards,<br>The MedIntern Team</p>
    </div>
</body>
</html>
''',
        'is_default': True,
        'available_variables': ['student_name', 'offer_title', 'hospital_name', 'status', 'status_color', 'message', 'application_link']
    }
]
