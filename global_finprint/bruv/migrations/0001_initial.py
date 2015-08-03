# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cruise', '0001_initial'),
        ('benthos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('drop_time', models.DateTimeField()),
                ('collection_time', models.DateTimeField(null=True)),
                ('time_bait_gone', models.DateTimeField(null=True)),
                ('depth', models.FloatField(null=True)),
                ('cruise', models.ForeignKey(to='cruise.Cruise')),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentMeasure',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('measurement_time', models.DateTimeField()),
                ('water_tmperature', models.FloatField(null=True)),
                ('salinity', models.FloatField(null=True)),
                ('conductivity', models.FloatField(null=True)),
                ('dissolved_oxygen', models.FloatField(null=True)),
                ('current_flow', models.FloatField(null=True)),
                ('deployment', models.ForeignKey(to='bruv.Deployment')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('camera', models.CharField(max_length=100, unique=True)),
                ('stereo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=100, unique=True)),
                ('genus', models.CharField(max_length=100, unique=True)),
                ('species', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('initial_observation_time', models.DateTimeField()),
                ('maximum_number_observed', models.IntegerField(null=True)),
                ('maximum_number_observed_time', models.DateTimeField(null=True)),
                ('stage', models.TextField(max_length=10, null=True)),
                ('activity', models.TextField(max_length=10, null=True)),
                ('deployment', models.ForeignKey(to='bruv.Deployment')),
                ('fish', models.ForeignKey(to='bruv.Fish')),
            ],
        ),
        migrations.CreateModel(
            name='ObservationImage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('observation', models.ForeignKey(to='bruv.Observation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('benthic', models.ForeignKey(to='benthos.Benthic')),
                ('cruises', models.ManyToManyField(to='cruise.Cruise', through='bruv.Deployment')),
            ],
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('site', models.ForeignKey(to='bruv.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('deployment', models.ForeignKey(to='bruv.Deployment')),
            ],
        ),
        migrations.AddField(
            model_name='siteimage',
            name='video',
            field=models.ForeignKey(to='bruv.Video'),
        ),
        migrations.AddField(
            model_name='observationimage',
            name='video',
            field=models.ForeignKey(to='bruv.Video'),
        ),
        migrations.AddField(
            model_name='observation',
            name='observer',
            field=models.ForeignKey(to='bruv.Observer'),
        ),
        migrations.AddField(
            model_name='deployment',
            name='equipment',
            field=models.ForeignKey(to='bruv.Equipment'),
        ),
        migrations.AddField(
            model_name='deployment',
            name='site',
            field=models.ForeignKey(to='bruv.Site'),
        ),
    ]
