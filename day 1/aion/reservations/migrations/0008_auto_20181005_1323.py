# Generated by Django 2.1.2 on 2018-10-05 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_auto_20181005_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='school_admin',
            field=models.BooleanField(default=False),
        ),
    ]