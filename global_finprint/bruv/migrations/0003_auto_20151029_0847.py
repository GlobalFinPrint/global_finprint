# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0002_auto_20151029_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(max_length=2, null=True, choices=[('SW', 'Southwest'), ('NE', 'Northeast'), ('W', 'West'), ('NW', 'Northwest'), ('SE', 'Southeast'), ('S', 'South'), ('E', 'East'), ('N', 'North')], help_text='compass direction'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(max_length=1, choices=[('U', 'Unknown'), ('F', 'Female'), ('M', 'Male')], default='U'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(max_length=2, choices=[('U', 'Unknown'), ('AD', 'Adult'), ('JU', 'Juvenile')], default='U'),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(max_length=3, choices=[('5', '5'), ('2', '2'), ('11', '11'), ('14', '14'), ('8', '8'), ('7', '7'), ('1', '1'), ('>15', '>15'), ('13', '13'), ('10', '10'), ('12', '12'), ('9', '9'), ('3', '3'), ('15', '15'), ('6', '6'), ('4', '4')]),
        ),
    ]
