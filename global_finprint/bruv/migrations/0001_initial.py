# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('habitat', '0001_initial'),
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drop',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('drop_time', models.DateTimeField()),
                ('collection_time', models.DateTimeField(null=True)),
                ('time_bait_gone', models.DateTimeField(null=True)),
                ('depth', models.FloatField(null=True)),
                ('benthic', models.ForeignKey(to='habitat.Benthic')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnvironmentMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('measurement_time', models.DateTimeField()),
                ('water_tmperature', models.FloatField(null=True)),
                ('salinity', models.FloatField(null=True)),
                ('conductivity', models.FloatField(null=True)),
                ('dissolved_oxygen', models.FloatField(null=True)),
                ('current_flow', models.FloatField(null=True)),
                ('deployment', models.ForeignKey(to='bruv.Drop')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('camera', models.CharField(max_length=100, unique=True)),
                ('stereo', models.BooleanField(default=False)),
                ('bruv', models.CharField(max_length=100, unique=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('family', models.CharField(max_length=100, unique=True)),
                ('genus', models.CharField(max_length=100, unique=True)),
                ('species', models.CharField(max_length=100, unique=True)),
                ('fishbase_key', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('initial_observation_time', models.DateTimeField()),
                ('maximum_number_observed', models.IntegerField(null=True)),
                ('maximum_number_observed_time', models.DateTimeField(null=True)),
                ('deployment', models.ForeignKey(to='bruv.Drop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObservationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('observation', models.ForeignKey(to='bruv.Observation')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObservedFish',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('sex', models.CharField(max_length=1, choices=[('U', 'Unknown'), ('F', 'Female'), ('M', 'Male')])),
                ('size', models.TextField(null=True, max_length=10)),
                ('stage', models.TextField(null=True, max_length=10)),
                ('activity', models.TextField(null=True, max_length=10)),
                ('behavior', models.TextField(null=True, max_length=50)),
                ('fish', models.ForeignKey(to='bruv.Fish')),
            ],
        ),
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('site', models.ForeignKey(to='bruv.Drop')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('deployment', models.ForeignKey(to='bruv.Drop')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
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
            name='observed_fish',
            field=models.ForeignKey(to='bruv.ObservedFish'),
        ),
        migrations.AddField(
            model_name='observation',
            name='observer',
            field=models.ForeignKey(to='bruv.Observer'),
        ),
        migrations.AddField(
            model_name='observation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drop',
            name='equipment',
            field=models.ForeignKey(to='bruv.Equipment'),
        ),
        migrations.AddField(
            model_name='drop',
            name='reef',
            field=models.ForeignKey(to='trip.Reef'),
        ),
        migrations.AddField(
            model_name='drop',
            name='trip',
            field=models.ForeignKey(to='trip.Trip'),
        ),
        migrations.AddField(
            model_name='drop',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
