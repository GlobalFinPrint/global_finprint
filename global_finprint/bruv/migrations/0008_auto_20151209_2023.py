# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0007_auto_20151208_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environmentmeasure',
            name='measurement_time',
        ),
        migrations.AlterField(
            model_name='animal',
            name='group',
            field=models.CharField(max_length=1, choices=[('S', 'Shark'), ('G', 'Groupers and jacks'), ('T', 'Other target'), ('R', 'Ray'), ('N', 'n/a')]),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(max_length=2, help_text='compass direction', choices=[('N', 'North'), ('SW', 'Southwest'), ('NE', 'Northeast'), ('E', 'East'), ('S', 'South'), ('NW', 'Northwest'), ('W', 'West'), ('SE', 'Southeast')], null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='surface_chop',
            field=models.CharField(max_length=1, choices=[('H', 'Heavy'), ('L', 'Light'), ('M', 'Medium')], null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='tide_state',
            field=models.CharField(max_length=3, choices=[('F', 'Flood'), ('S2E', 'Slack to Ebb'), ('S2F', 'Slack to Flood'), ('S', 'Slack'), ('E', 'Ebb')], null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='wind_direction',
            field=models.CharField(max_length=2, help_text='compass direction', choices=[('N', 'North'), ('SW', 'Southwest'), ('NE', 'Northeast'), ('E', 'East'), ('S', 'South'), ('NW', 'Northwest'), ('W', 'West'), ('SE', 'Southeast')], null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='bait_container',
            field=models.CharField(max_length=1, default='C', choices=[('C', 'Cage'), ('B', 'Bag')]),
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(max_length=1, default='U', choices=[('U', 'Unknown'), ('F', 'Female'), ('M', 'Male')]),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(max_length=2, default='U', choices=[('AD', 'Adult'), ('U', 'Unknown'), ('JU', 'Juvenile')]),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(max_length=3, choices=[('14', '14'), ('15', '15'), ('10', '10'), ('12', '12'), ('8', '8'), ('7', '7'), ('11', '11'), ('9', '9'), ('4', '4'), ('1', '1'), ('>15', '>15'), ('5', '5'), ('3', '3'), ('2', '2'), ('13', '13'), ('6', '6')]),
        ),
    ]
