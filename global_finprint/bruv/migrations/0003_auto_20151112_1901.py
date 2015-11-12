# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0002_auto_20151112_1901'),
        ('bruv', '0002_auto_20151102_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='group',
            field=models.CharField(choices=[('G', 'Groupers and jacks'), ('R', 'Ray'), ('N', 'n/a'), ('T', 'Other target'), ('S', 'Shark')], default='S', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='animal',
            name='rank',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='animal',
            name='region',
            field=models.ForeignKey(default=1, to='habitat.Region'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='animal',
            name='family',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='animal',
            name='fishbase_key',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='genus',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='animal',
            name='sealifebase_key',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='species',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(choices=[('S', 'South'), ('W', 'West'), ('SE', 'Southeast'), ('E', 'East'), ('NW', 'Northwest'), ('SW', 'Southwest'), ('NE', 'Northeast'), ('N', 'North')], null=True, max_length=2, help_text='compass direction'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='bait_container',
            field=models.CharField(choices=[('B', 'Bag'), ('C', 'Cage')], default='C', max_length=1),
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unknown')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(choices=[('JU', 'Juvenile'), ('U', 'Unknown'), ('AD', 'Adult')], default='U', max_length=2),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(choices=[('>15', '>15'), ('1', '1'), ('14', '14'), ('9', '9'), ('15', '15'), ('10', '10'), ('7', '7'), ('5', '5'), ('13', '13'), ('8', '8'), ('3', '3'), ('2', '2'), ('4', '4'), ('11', '11'), ('12', '12'), ('6', '6')], max_length=3),
        ),
        migrations.AlterUniqueTogether(
            name='animal',
            unique_together=set([('genus', 'species')]),
        ),
    ]
