
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('internships', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquired_skills_grade', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('supervision_satisfaction_grade', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('working_conditions_grade', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('acquired_skills', models.JSONField(blank=True, default=list)),
                ('difficulties_encountered', models.TextField(blank=True, null=True)),
                ('positive_points', models.TextField(blank=True, null=True)),
                ('improvement_suggestions', models.TextField(blank=True, null=True)),
                ('professional_project', models.TextField(blank=True, null=True)),
                ('submission_date', models.DateTimeField(blank=True, null=True)),
                ('is_submitted', models.BooleanField(default=False)),
                ('internship', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auto_evaluation', to='internships.internship')),
            ],
            options={
                'verbose_name_plural': 'Auto-evaluations',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technical_skills', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('attendance_punctuality', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('patient_relation', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('teamwork', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('initiative_autonomy', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('theoretical_knowledge', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('final_grade', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('overall_appreciation', models.TextField(blank=True, null=True)),
                ('strengths', models.JSONField(blank=True, default=list)),
                ('areas_for_improvement', models.JSONField(blank=True, default=list)),
                ('recommendations', models.TextField(blank=True, null=True)),
                ('suitable_for_next_internship', models.BooleanField(blank=True, null=True)),
                ('recommend_for_supervision', models.BooleanField(blank=True, null=True)),
                ('thesis_opinion', models.TextField(blank=True, null=True)),
                ('evaluation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_submitted', models.BooleanField(default=False)),
                ('is_validated', models.BooleanField(default=False)),
                ('validation_date', models.DateTimeField(blank=True, null=True)),
                ('supervisor_signature', models.BooleanField(default=False)),
                ('student_signature', models.BooleanField(default=False)),
                ('admin_signature', models.BooleanField(default=False)),
                ('internship', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation', to='internships.internship')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_evaluations', to=settings.AUTH_USER_MODEL)),
                ('validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validated_evaluations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Evaluations',
                'ordering': ['-evaluation_date'],
            },
        ),
    ]
