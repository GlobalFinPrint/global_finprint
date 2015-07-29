# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('benthos', '0001_initial'),
        ('cruise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('drop_time', models.DateTimeField()),
                ('collection_time', models.DateTimeField()),
                ('time_bait_gone', models.DateTimeField()),
                ('depth', models.FloatField()),
                ('cruise', models.ForeignKey(to='cruise.Cruise')),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('measurement_time', models.DateTimeField()),
                ('water_tmperature', models.FloatField()),
                ('salinity', models.FloatField()),
                ('conductivity', models.FloatField()),
                ('dissolved_oxygen', models.FloatField()),
                ('current_flow', models.FloatField()),
                ('deployment', models.ForeignKey(to='bruv.Deployment')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('camera', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('family', models.CharField(max_length=100, unique=True)),
                ('genus', models.CharField(max_length=100, unique=True)),
                ('species', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('measurement_time', models.DateTimeField()),
                ('water_tmperature', models.FloatField()),
                ('salinity', models.FloatField()),
                ('conductivity', models.FloatField()),
                ('dissolved_oxygen', models.FloatField()),
                ('current_flow', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('benthic_category', models.ForeignKey(to='benthos.BenthicCategory')),
                ('cruises', models.ManyToManyField(to='cruise.Cruise', through='bruv.Deployment')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
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
        migrations.AddField(
            model_name='deployment',
            name='video',
            field=models.ForeignKey(to='bruv.Video'),
        ),
    ]
