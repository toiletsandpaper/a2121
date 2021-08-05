# Generated by Django 2.1.2 on 2019-01-29 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0013_auto_20190129_1318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='block',
            options={'ordering': ['name', 'sequence']},
        ),
        migrations.AlterField(
            model_name='block',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Block Name'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Resource Name'),
        ),
    ]