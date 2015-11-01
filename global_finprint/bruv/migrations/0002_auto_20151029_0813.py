# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipment',
            options={'verbose_name_plural': 'Equipment'},
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(help_text='compass direction', choices=[('N', 'North'), ('NW', 'Northwest'), ('W', 'West'), ('NE', 'Northeast'), ('SE', 'Southeast'), ('E', 'East'), ('SW', 'Southwest'), ('S', 'South')], null=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='bait_container',
            field=models.CharField(choices=[('C', 'Cage'), ('B', 'Bag')], max_length=1, default='C'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unknown')], max_length=1, default='U'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(choices=[('JU', 'Juvenile'), ('AD', 'Adult'), ('U', 'Unknown')], max_length=2, default='U'),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(choices=[('12', '12'), ('14', '14'), ('8', '8'), ('7', '7'), ('11', '11'), ('5', '5'), ('13', '13'), ('10', '10'), ('3', '3'), ('2', '2'), ('1', '1'), ('4', '4'), ('>15', '>15'), ('15', '15'), ('9', '9'), ('6', '6')], max_length=3),
        ),
    ]
