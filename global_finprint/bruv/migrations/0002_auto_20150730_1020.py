# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('video', models.ForeignKey(to='bruv.Video')),
            ],
        ),
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='observation',
            name='conductivity',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='current_flow',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='dissolved_oxygen',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='measurement_time',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='salinity',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='water_tmperature',
        ),
        migrations.AddField(
            model_name='observation',
            name='deployment',
            field=models.ForeignKey(default=1, to='bruv.Deployment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='fish',
            field=models.ForeignKey(default=1, to='bruv.Fish'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='initial_observation_time',
            field=models.DateTimeField(default=datetime.datetime.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='maximum_number_observed',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='maximum_number_observed_time',
            field=models.DateTimeField(default=datetime.datetime.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='image',
            field=models.ForeignKey(default=1, to='bruv.Image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='observer',
            field=models.ForeignKey(default=1, to='bruv.Observer'),
            preserve_default=False,
        ),
    ]
