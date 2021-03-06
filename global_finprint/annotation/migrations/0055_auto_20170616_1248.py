# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-16 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0054_auto_20170616_0945'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='attribute',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='globalattribute',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='animalobservation',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='animalobservation',
            name='stage',
            field=models.CharField(choices=[('AD', 'Adult'), ('JU', 'Juvenile'), ('U', 'Unknown')], default='U', max_length=2),
        ),
        migrations.AlterField(
            model_name='masteranimalobservation',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='masteranimalobservation',
            name='stage',
            field=models.CharField(choices=[('AD', 'Adult'), ('JU', 'Juvenile'), ('U', 'Unknown')], default='U', max_length=2),
        ),
        migrations.AlterField(
            model_name='masterobservation',
            name='type',
            field=models.CharField(choices=[('A', 'Animal'), ('I', 'Of interest')], default='I', max_length=1),
        ),
        migrations.AlterField(
            model_name='observation',
            name='type',
            field=models.CharField(choices=[('A', 'Animal'), ('I', 'Of interest')], default='I', max_length=1),
        ),
    ]
