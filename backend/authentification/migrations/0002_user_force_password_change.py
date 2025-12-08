
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='force_password_change',
            field=models.BooleanField(default=True),
        ),
    ]
