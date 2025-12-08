
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
        ('internships', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='internships.internshipoffer'),
        ),
        migrations.AddField(
            model_name='application',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='users.studentprofile'),
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together={('student', 'offer')},
        ),
    ]
