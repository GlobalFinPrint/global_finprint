# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-15 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0008_auto_20160310_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='rank',
            field=models.PositiveIntegerField(blank=True, null=True),
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
            model_name='observation',
            name='type',
            field=models.CharField(choices=[('A', 'Animal'), ('I', 'Of interest')], default='I', max_length=1),
        ),
        migrations.AlterField(
            model_name='videoannotator',
            name='status',
            field=models.CharField(choices=[('R', 'Ready for review'), ('D', 'Disabled'), ('C', 'Competed'), ('I', 'In progress'), ('N', 'Not started')], default='N', max_length=1),
        ),
    ]
