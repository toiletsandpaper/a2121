# Generated by Django 2.1.2 on 2019-01-04 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0009_block_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
