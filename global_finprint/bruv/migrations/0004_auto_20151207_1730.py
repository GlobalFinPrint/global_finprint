# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0003_auto_20151112_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='group',
            field=models.CharField(max_length=1, choices=[('T', 'Other target'), ('S', 'Shark'), ('N', 'n/a'), ('G', 'Groupers and jacks'), ('R', 'Ray')]),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(help_text='compass direction', choices=[('W', 'West'), ('SW', 'Southwest'), ('NW', 'Northwest'), ('S', 'South'), ('SE', 'Southeast'), ('NE', 'Northeast'), ('N', 'North'), ('E', 'East')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='water_temperature',
            field=models.DecimalField(decimal_places=1, help_text='C', null=True, max_digits=4),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='bait_container',
            field=models.CharField(max_length=1, choices=[('C', 'Cage'), ('B', 'Bag')], default='C'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(max_length=1, choices=[('M', 'Male'), ('U', 'Unknown'), ('F', 'Female')], default='U'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(max_length=2, choices=[('U', 'Unknown'), ('AD', 'Adult'), ('JU', 'Juvenile')], default='U'),
        ),
        migrations.AlterField(
            model_name='set',
            name='depth',
            field=models.FloatField(help_text='m', null=True),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(max_length=3, choices=[('>15', '>15'), ('8', '8'), ('7', '7'), ('4', '4'), ('3', '3'), ('13', '13'), ('1', '1'), ('15', '15'), ('12', '12'), ('10', '10'), ('2', '2'), ('14', '14'), ('9', '9'), ('5', '5'), ('11', '11'), ('6', '6')]),
        ),
    ]
