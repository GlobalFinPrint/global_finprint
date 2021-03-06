# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-25 23:16
from __future__ import unicode_literals

import config.current_user
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0019_auto_20161025_2316'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20160412_2234'),
        ('annotation', '0025_auto_20160920_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterAnimalObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('U', 'Unknown'), ('F', 'Female')], default='U', max_length=1)),
                ('stage', models.CharField(choices=[('AD', 'Adult'), ('JU', 'Juvenile'), ('U', 'Unknown')], default='U', max_length=2)),
                ('length', models.IntegerField(help_text='centimeters', null=True)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.Animal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MasterEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('event_time', models.IntegerField(default=0, help_text='ms')),
                ('extent', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326)),
                ('note', models.TextField(null=True)),
                ('attribute', models.ManyToManyField(to='annotation.Attribute')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MasterObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('I', 'Of interest'), ('A', 'Animal')], default='I', max_length=1)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('comment', models.TextField(null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master_observations_created', to='core.FinprintUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MasterRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('note', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('deprecated', models.BooleanField(default=False)),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bruv.Set')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='masterobservation',
            name='master_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.MasterRecord'),
        ),
        migrations.AddField(
            model_name='masterobservation',
            name='original',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.Observation'),
        ),
        migrations.AddField(
            model_name='masterobservation',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master_observations_updated', to='core.FinprintUser'),
        ),
        migrations.AddField(
            model_name='masterobservation',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='masterevent',
            name='master_observation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.MasterObservation'),
        ),
        migrations.AddField(
            model_name='masterevent',
            name='original',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.Event'),
        ),
        migrations.AddField(
            model_name='masterevent',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='masteranimalobservation',
            name='master_observation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='annotation.MasterObservation'),
        ),
        migrations.AddField(
            model_name='masteranimalobservation',
            name='original',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.AnimalObservation'),
        ),
        migrations.AddField(
            model_name='masteranimalobservation',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
