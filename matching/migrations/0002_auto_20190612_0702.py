# Generated by Django 2.1.7 on 2019-06-12 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='avg_age',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='team',
            name='hope_age',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]
