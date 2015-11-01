# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_auto_20151029_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='reef',
            name='fishing_restrictions',
            field=models.ManyToManyField(blank=True, null=True, to='trip.FishingRestrictions'),
        ),
        migrations.AlterField(
            model_name='reef',
            name='mpa',
            field=models.ForeignKey(null=True, blank=True, to='trip.MPA'),
        ),
        migrations.RemoveField(
            model_name='reef',
            name='shark_gear_in_use',
        ),
        migrations.AddField(
            model_name='reef',
            name='shark_gear_in_use',
            field=models.ManyToManyField(blank=True, null=True, to='trip.SharkGearInUse'),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(max_length=16, choices=[('C', 'Continental'), ('I', 'Island'), ('A', 'Atoll')]),
        ),
        migrations.AlterField(
            model_name='trip',
            name='boat',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
