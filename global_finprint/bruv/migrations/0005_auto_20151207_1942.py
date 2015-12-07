# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0004_auto_20151207_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='tide_state',
        ),
        migrations.AddField(
            model_name='environmentmeasure',
            name='cloud_cover',
            field=models.IntegerField(help_text='%', null=True),
        ),
        migrations.AddField(
            model_name='environmentmeasure',
            name='surface_chop',
            field=models.CharField(max_length=1, choices=[('L', 'Light'), ('H', 'Heavy'), ('M', 'Medium')], null=True),
        ),
        migrations.AddField(
            model_name='environmentmeasure',
            name='tide_state',
            field=models.CharField(max_length=3, choices=[('S', 'Slack'), ('S2E', 'Slack to Ebb'), ('S2F', 'Slack to Flood'), ('E', 'Ebb'), ('F', 'Flood')], null=True),
        ),
        migrations.AddField(
            model_name='environmentmeasure',
            name='wind_direction',
            field=models.CharField(choices=[('W', 'West'), ('NW', 'Northwest'), ('S', 'South'), ('NE', 'Northeast'), ('SW', 'Southwest'), ('E', 'East'), ('N', 'North'), ('SE', 'Southeast')], max_length=2, help_text='compass direction', null=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='group',
            field=models.CharField(max_length=1, choices=[('R', 'Ray'), ('N', 'n/a'), ('S', 'Shark'), ('T', 'Other target'), ('G', 'Groupers and jacks')]),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(choices=[('W', 'West'), ('NW', 'Northwest'), ('S', 'South'), ('NE', 'Northeast'), ('SW', 'Southwest'), ('E', 'East'), ('N', 'North'), ('SE', 'Southeast')], max_length=2, help_text='compass direction', null=True),
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'Unknown'), ('F', 'Female'), ('M', 'Male')]),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(max_length=3, choices=[('7', '7'), ('4', '4'), ('2', '2'), ('13', '13'), ('6', '6'), ('3', '3'), ('14', '14'), ('12', '12'), ('11', '11'), ('9', '9'), ('1', '1'), ('>15', '>15'), ('10', '10'), ('8', '8'), ('5', '5'), ('15', '15')]),
        ),
    ]
