# Generated by Django 2.1.2 on 2018-10-05 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20181005_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, help_text='About Me', max_length=500, null=True),
        ),
    ]