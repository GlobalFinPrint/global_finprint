# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-16 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0027_auto_20170616_0945'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='benthiccategory',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='settag',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(blank=True, choices=[('E', 'East'), ('SW', 'Southwest'), ('SE', 'Southeast'), ('NE', 'Northeast'), ('N', 'North'), ('NW', 'Northwest'), ('S', 'South'), ('W', 'West')], help_text='compass direction', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='surface_chop',
            field=models.CharField(blank=True, choices=[('M', 'Medium'), ('L', 'Light'), ('H', 'Heavy')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='tide_state',
            field=models.CharField(blank=True, choices=[('S', 'Slack'), ('F', 'Flood'), ('S2E', 'Slack to Ebb'), ('S2F', 'Slack to Flood'), ('E', 'Ebb')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='wind_direction',
            field=models.CharField(blank=True, choices=[('E', 'East'), ('SW', 'Southwest'), ('SE', 'Southeast'), ('NE', 'Northeast'), ('N', 'North'), ('NW', 'Northwest'), ('S', 'South'), ('W', 'West')], help_text='compass direction', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='bait_container',
            field=models.CharField(choices=[('B', 'Bag'), ('C', 'Cage')], default='C', max_length=1),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(choices=[('11', '11'), ('1', '1'), ('12', '12'), ('>15', '>15'), ('9', '9'), ('8', '8'), ('7', '7'), ('5', '5'), ('13', '13'), ('10', '10'), ('14', '14'), ('6', '6'), ('3', '3'), ('2', '2'), ('0', 'LEGACY'), ('4', '4'), ('15', '15')], help_text='m', max_length=3),
        ),
    ]