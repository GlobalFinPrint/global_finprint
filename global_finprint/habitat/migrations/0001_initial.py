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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MPA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('area', models.PositiveIntegerField(help_text='km^2')),
                ('founded', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'MPA',
                'verbose_name_plural': 'MPAs',
            },
        ),
        migrations.CreateModel(
            name='MPACompliance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=48)),
            ],
            options={
                'verbose_name': 'MPA compliance',
                'verbose_name_plural': 'MPA compliance',
            },
        ),
        migrations.CreateModel(
            name='MPAIsolation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=24)),
            ],
            options={
                'verbose_name': 'MPA isolation',
                'verbose_name_plural': 'MPA isolation',
            },
        ),
        migrations.CreateModel(
            name='ProtectionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('fishing_restrictions', models.ManyToManyField(to='habitat.FishingRestrictions', blank=True)),
                ('mpa', models.ForeignKey(to='habitat.MPA', null=True, blank=True)),
                ('protection_status', models.ForeignKey(to='habitat.ProtectionStatus')),
            ],
        ),
        migrations.CreateModel(
            name='ReefType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=48)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('boundary', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('type', models.CharField(choices=[('C', 'Continental'), ('A', 'Atoll'), ('I', 'Island')], max_length=16)),
                ('location', models.ForeignKey(to='habitat.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Substrate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=24, unique=True)),
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
