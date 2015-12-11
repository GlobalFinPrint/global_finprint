# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0006_auto_20151207_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environmentmeasure',
            name='set',
        ),
        migrations.AddField(
            model_name='set',
            name='drop_measure',
            field=models.OneToOneField(to='bruv.EnvironmentMeasure', blank=True, related_name='drop_parent_set', null=True),
        ),
        migrations.AddField(
            model_name='set',
            name='haul_measure',
            field=models.OneToOneField(to='bruv.EnvironmentMeasure', blank=True, related_name='haul_parent_set', null=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='group',
            field=models.CharField(max_length=1, choices=[('G', 'Groupers and jacks'), ('T', 'Other target'), ('S', 'Shark'), ('R', 'Ray'), ('N', 'n/a')]),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(choices=[('NE', 'Northeast'), ('S', 'South'), ('SE', 'Southeast'), ('W', 'West'), ('E', 'East'), ('NW', 'Northwest'), ('SW', 'Southwest'), ('N', 'North')], max_length=2, null=True, help_text='compass direction'),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='surface_chop',
            field=models.CharField(choices=[('M', 'Medium'), ('H', 'Heavy'), ('L', 'Light')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='tide_state',
            field=models.CharField(choices=[('E', 'Ebb'), ('S2F', 'Slack to Flood'), ('S2E', 'Slack to Ebb'), ('F', 'Flood'), ('S', 'Slack')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='wind_direction',
            field=models.CharField(choices=[('NE', 'Northeast'), ('S', 'South'), ('SE', 'Southeast'), ('W', 'West'), ('E', 'East'), ('NW', 'Northwest'), ('SW', 'Southwest'), ('N', 'North')], max_length=2, null=True, help_text='compass direction'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='bait_container',
            field=models.CharField(default='C', max_length=1, choices=[('B', 'Bag'), ('C', 'Cage')]),
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(default='U', max_length=1, choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(default='U', max_length=2, choices=[('JU', 'Juvenile'), ('AD', 'Adult'), ('U', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(max_length=3, choices=[('15', '15'), ('>15', '>15'), ('6', '6'), ('12', '12'), ('5', '5'), ('11', '11'), ('14', '14'), ('10', '10'), ('7', '7'), ('4', '4'), ('3', '3'), ('13', '13'), ('8', '8'), ('2', '2'), ('9', '9'), ('1', '1')]),
        ),
    ]
