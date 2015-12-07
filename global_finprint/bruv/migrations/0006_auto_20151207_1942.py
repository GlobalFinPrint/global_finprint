# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0005_auto_20151207_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='environmentmeasure',
            name='estimated_wind_speed',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='group',
            field=models.CharField(choices=[('S', 'Shark'), ('N', 'n/a'), ('R', 'Ray'), ('G', 'Groupers and jacks'), ('T', 'Other target')], max_length=1),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(help_text='compass direction', choices=[('NW', 'Northwest'), ('W', 'West'), ('NE', 'Northeast'), ('SW', 'Southwest'), ('SE', 'Southeast'), ('E', 'East'), ('N', 'North'), ('S', 'South')], null=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='surface_chop',
            field=models.CharField(choices=[('H', 'Heavy'), ('M', 'Medium'), ('L', 'Light')], null=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='tide_state',
            field=models.CharField(choices=[('E', 'Ebb'), ('S2F', 'Slack to Flood'), ('F', 'Flood'), ('S2E', 'Slack to Ebb'), ('S', 'Slack')], null=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='wind_direction',
            field=models.CharField(help_text='compass direction', choices=[('NW', 'Northwest'), ('W', 'West'), ('NE', 'Northeast'), ('SW', 'Southwest'), ('SE', 'Southeast'), ('E', 'East'), ('N', 'North'), ('S', 'South')], null=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(choices=[('10', '10'), ('13', '13'), ('3', '3'), ('12', '12'), ('1', '1'), ('>15', '>15'), ('15', '15'), ('8', '8'), ('7', '7'), ('4', '4'), ('11', '11'), ('14', '14'), ('9', '9'), ('5', '5'), ('2', '2'), ('6', '6')], max_length=3),
        ),
    ]
