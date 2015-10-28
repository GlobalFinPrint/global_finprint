# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import config.current_user
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(max_length=100)),
                ('family', models.CharField(unique=True, max_length=100)),
                ('genus', models.CharField(unique=True, max_length=100)),
                ('species', models.CharField(unique=True, max_length=100)),
                ('fishbase_key', models.IntegerField(null=True)),
                ('sealifebase_key', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('measurement_time', models.DateTimeField()),
                ('water_temperature', models.IntegerField(null=True)),
                ('salinity', models.FloatField(null=True)),
                ('conductivity', models.FloatField(null=True)),
                ('dissolved_oxygen', models.FloatField(null=True)),
                ('current_flow', models.FloatField(null=True)),
                ('current_direction', models.FloatField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('camera', models.CharField(max_length=100)),
                ('stereo', models.BooleanField(default=False)),
                ('frame_type', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('initial_observation_time', models.DateTimeField()),
                ('sex', models.CharField(choices=[('U', 'Unknown'), ('F', 'Female'), ('M', 'Male')], default='U', max_length=1)),
                ('stage', models.CharField(choices=[('U', 'Unknown'), ('AD', 'Adult'), ('JU', 'Juvenile')], default='U', max_length=2)),
                ('length', models.IntegerField(null=True, help_text='centimeters')),
                ('behavior', models.CharField(null=True, max_length=50, blank=True)),
                ('animal', models.ForeignKey(to='bruv.Animal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObservationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('observation', models.ForeignKey(to='bruv.Observation')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('drop_time', models.DateTimeField()),
                ('collection_time', models.DateTimeField(null=True, blank=True)),
                ('depth', models.FloatField(null=True)),
                ('bait', models.CharField(max_length=100)),
                ('equipment', models.ForeignKey(to='bruv.Equipment')),
                ('reef', models.ForeignKey(null=True, to='trip.Reef')),
                ('trip', models.ForeignKey(to='trip.Trip')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('set', models.ForeignKey(to='bruv.Set')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('length', models.FloatField()),
                ('set', models.ForeignKey(to='bruv.Set')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
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
            name='observer',
            field=models.ForeignKey(to='bruv.Observer'),
        ),
        migrations.AddField(
            model_name='observation',
            name='set',
            field=models.ForeignKey(to='bruv.Set'),
        ),
        migrations.AddField(
            model_name='observation',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='environmentmeasure',
            name='set',
            field=models.ForeignKey(to='bruv.Set'),
        ),
        migrations.AddField(
            model_name='environmentmeasure',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL),
        ),
    ]
