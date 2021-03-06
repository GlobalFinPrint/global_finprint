# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-20 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0038_dummy_column'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bait',
            name='type',
            field=models.CharField(choices=[('WHL', 'Whole'), ('CRS', 'Crushed'), ('CHP', 'Chopped')], max_length=3),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(blank=True, choices=[('N', 'North'), ('NW', 'Northwest'), ('SW', 'Southwest'), ('E', 'East'), ('S', 'South'), ('W', 'West'), ('SE', 'Southeast'), ('NE', 'Northeast')], help_text='compass direction', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='surface_chop',
            field=models.CharField(blank=True, choices=[('H', 'Heavy'), ('M', 'Medium'), ('L', 'Light')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='tide_state',
            field=models.CharField(blank=True, choices=[('S2E', 'Slack to Ebb'), ('S', 'Slack'), ('E', 'Ebb'), ('F', 'Flood'), ('S2F', 'Slack to Flood')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='wind_direction',
            field=models.CharField(blank=True, choices=[('N', 'North'), ('NW', 'Northwest'), ('SW', 'Southwest'), ('E', 'East'), ('S', 'South'), ('W', 'West'), ('SE', 'Southeast'), ('NE', 'Northeast')], help_text='compass direction', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='set',
            name='field_of_view',
            field=models.CharField(blank=True, choices=[('FD', 'Facing Down'), ('L', 'Limited'), ('O', 'Open'), ('FU', 'Facing Up')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(blank=True, choices=[('V6-8', 'V6-8'), ('V4-6', 'V4-6'), ('V2-4', 'V2-4'), ('V10+', 'V10+'), ('V8-10', 'V8-10'), ('V0-2', 'V0-2')], db_column='visibility_str', max_length=10, null=True),
        ),
    ]
