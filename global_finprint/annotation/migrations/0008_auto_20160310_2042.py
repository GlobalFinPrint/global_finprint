# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-10 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0007_auto_20160303_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservationFeature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feature', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='animalobservation',
            name='external_parasites',
        ),
        migrations.RemoveField(
            model_name='animalobservation',
            name='gear_fouled',
        ),
        migrations.RemoveField(
            model_name='animalobservation',
            name='gear_on_animal',
        ),
        migrations.RemoveField(
            model_name='animalobservation',
            name='tag',
        ),
        migrations.AddField(
            model_name='animalobservation',
            name='features',
            field=models.ManyToManyField(to='annotation.ObservationFeature'),
        ),
    ]
