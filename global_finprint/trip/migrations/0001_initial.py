# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import config.current_user
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FishingRestrictions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name_plural': 'Fishing restrictions',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MPA',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('area', models.PositiveIntegerField(help_text='km^2')),
                ('founded', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name_plural': 'MPAs',
                'verbose_name': 'MPA',
            },
        ),
        migrations.CreateModel(
            name='MPACompliance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=24)),
            ],
            options={
                'verbose_name_plural': 'MPA compliance',
                'verbose_name': 'MPA compliance',
            },
        ),
        migrations.CreateModel(
            name='MPAIsolation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=24)),
            ],
            options={
                'verbose_name_plural': 'MPA isolation',
                'verbose_name': 'MPA isolation',
            },
        ),
        migrations.CreateModel(
            name='ProtectionStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name_plural': 'Protection status',
            },
        ),
        migrations.CreateModel(
            name='Reef',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('mpa', models.ForeignKey(null=True, to='trip.MPA')),
                ('protection_status', models.ForeignKey(to='trip.ProtectionStatus')),
            ],
        ),
        migrations.CreateModel(
            name='ReefType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SharkGearInUse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=24)),
            ],
            options={
                'verbose_name_plural': 'Shark gear in use',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('type', models.CharField(max_length=16, choices=[('A', 'Atoll'), ('I', 'Island'), ('C', 'Continental')])),
                ('location', models.ForeignKey(to='trip.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('association', models.CharField(max_length=100)),
                ('lead', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('boat', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', models.ForeignKey(to='trip.Location')),
                ('team', models.ForeignKey(to='trip.Team')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reef',
            name='shark_gear_in_use',
            field=models.ForeignKey(null=True, to='trip.SharkGearInUse'),
        ),
        migrations.AddField(
            model_name='reef',
            name='site',
            field=models.ForeignKey(to='trip.Site'),
        ),
        migrations.AddField(
            model_name='reef',
            name='type',
            field=models.ForeignKey(to='trip.ReefType'),
        ),
        migrations.AddField(
            model_name='mpa',
            name='mpa_compliance',
            field=models.ForeignKey(to='trip.MPACompliance'),
        ),
        migrations.AddField(
            model_name='mpa',
            name='mpa_isolation',
            field=models.ForeignKey(to='trip.MPAIsolation'),
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(to='trip.Region'),
        ),
    ]
