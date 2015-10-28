# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import config.current_user
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FishingRestrictions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MPA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('area', models.PositiveIntegerField(help_text='km^2')),
                ('founded', models.PositiveIntegerField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='MPACompliance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='MPAIsolation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='ProtectionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Reef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('mpa', models.ForeignKey(null=True, to='trip.MPA')),
                ('protection_status', models.ForeignKey(to='trip.ProtectionStatus')),
            ],
        ),
        migrations.CreateModel(
            name='ReefType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SharkGearInUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('type', models.CharField(choices=[('I', 'Island'), ('C', 'Continental'), ('A', 'Atoll')], max_length=16)),
                ('location', models.ForeignKey(to='trip.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
