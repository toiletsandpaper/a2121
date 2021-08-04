# Generated by Django 2.1.2 on 2019-02-01 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0020_announcement_system_wide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.School'),
        ),
    ]
