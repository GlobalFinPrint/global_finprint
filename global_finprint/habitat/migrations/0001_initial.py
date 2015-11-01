# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FishingRestrictions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=48)),
            ],
            options={
                'verbose_name_plural': 'Fishing restrictions',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MPA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=48)),
            ],
            options={
                'verbose_name_plural': 'MPA compliance',
                'verbose_name': 'MPA compliance',
            },
        ),
        migrations.CreateModel(
            name='MPAIsolation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=48)),
            ],
            options={
                'verbose_name_plural': 'Protection status',
            },
        ),
        migrations.CreateModel(
            name='Reef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('fishing_restrictions', models.ManyToManyField(to='habitat.FishingRestrictions', blank=True)),
                ('mpa', models.ForeignKey(blank=True, null=True, to='habitat.MPA')),
                ('protection_status', models.ForeignKey(to='habitat.ProtectionStatus')),
            ],
        ),
        migrations.CreateModel(
            name='ReefType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SharkGearInUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=24)),
                ('description', models.CharField(max_length=48)),
            ],
            options={
                'verbose_name_plural': 'Shark gear in use',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('type', models.CharField(choices=[('A', 'Atoll'), ('I', 'Island'), ('C', 'Continental')], max_length=16)),
                ('location', models.ForeignKey(to='habitat.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Substrate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(unique=True, max_length=24)),
            ],
        ),
        migrations.AddField(
            model_name='reef',
            name='shark_gear_in_use',
            field=models.ManyToManyField(to='habitat.SharkGearInUse', blank=True),
        ),
        migrations.AddField(
            model_name='reef',
            name='site',
            field=models.ForeignKey(to='habitat.Site'),
        ),
        migrations.AddField(
            model_name='reef',
            name='type',
            field=models.ForeignKey(to='habitat.ReefType'),
        ),
        migrations.AddField(
            model_name='mpa',
            name='mpa_compliance',
            field=models.ForeignKey(to='habitat.MPACompliance'),
        ),
        migrations.AddField(
            model_name='mpa',
            name='mpa_isolation',
            field=models.ForeignKey(to='habitat.MPAIsolation'),
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(to='habitat.Region'),
        ),
    ]
