# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-20 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0061_auto_20180416_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalobservation',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('U', 'Unknown'), ('F', 'Female')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='animalobservation',
            name='stage',
            field=models.CharField(choices=[('U', 'Unknown'), ('JU', 'Juvenile'), ('AD', 'Adult')], default='U', max_length=2),
        ),
        migrations.AlterField(
            model_name='masteranimalobservation',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('U', 'Unknown'), ('F', 'Female')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='masteranimalobservation',
            name='stage',
            field=models.CharField(choices=[('U', 'Unknown'), ('JU', 'Juvenile'), ('AD', 'Adult')], default='U', max_length=2),
        ),
    ]
