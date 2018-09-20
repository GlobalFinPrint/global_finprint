# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-20 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0064_dummy_column'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalobservation',
            name='sex',
            field=models.CharField(choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='animalobservation',
            name='stage',
            field=models.CharField(choices=[('AD', 'Adult'), ('U', 'Unknown'), ('JU', 'Juvenile')], default='U', max_length=2),
        ),
        migrations.AlterField(
            model_name='masteranimalobservation',
            name='sex',
            field=models.CharField(choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='masteranimalobservation',
            name='stage',
            field=models.CharField(choices=[('AD', 'Adult'), ('U', 'Unknown'), ('JU', 'Juvenile')], default='U', max_length=2),
        ),
    ]
