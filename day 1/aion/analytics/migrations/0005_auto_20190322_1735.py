# Generated by Django 2.1.2 on 2019-03-22 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0029_auto_20190322_1323'),
        ('analytics', '0004_auto_20190322_1734'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LifetimeAionStats',
            new_name='LifetimeAionStat',
        ),
        migrations.RenameModel(
            old_name='LifetimeSchoolStats',
            new_name='LifetimeSchoolStat',
        ),
    ]