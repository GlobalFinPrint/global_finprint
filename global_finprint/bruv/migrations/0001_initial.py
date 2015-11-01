# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import config.current_user
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0001_initial'),
        ('trip', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('common_name', models.CharField(max_length=100)),
                ('family', models.CharField(unique=True, max_length=100)),
                ('genus', models.CharField(unique=True, max_length=100)),
                ('species', models.CharField(unique=True, max_length=100)),
                ('fishbase_key', models.IntegerField(null=True)),
                ('sealifebase_key', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalBehavior',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('measurement_time', models.DateTimeField()),
                ('water_temperature', models.IntegerField(null=True, help_text='C')),
                ('salinity', models.DecimalField(null=True, max_digits=4, decimal_places=2, help_text='ppt')),
                ('conductivity', models.DecimalField(null=True, max_digits=4, decimal_places=2, help_text='S/m')),
                ('dissolved_oxygen', models.DecimalField(null=True, max_digits=3, decimal_places=1, help_text='%')),
                ('current_flow', models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text='m/s')),
                ('current_direction', models.CharField(null=True, choices=[('E', 'East'), ('S', 'South'), ('SE', 'Southeast'), ('NE', 'Northeast'), ('W', 'West'), ('N', 'North'), ('SW', 'Southwest'), ('NW', 'Northwest')], max_length=2, help_text='compass direction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('camera', models.CharField(max_length=16)),
                ('stereo', models.BooleanField(default=False)),
                ('bait_container', models.CharField(choices=[('B', 'Bag'), ('C', 'Cage')], default='C', max_length=1)),
                ('arm_length', models.PositiveIntegerField(help_text='centimeters')),
                ('camera_height', models.PositiveIntegerField(help_text='centimeters')),
            ],
            options={
                'verbose_name_plural': 'Equipment',
            },
        ),
        migrations.CreateModel(
            name='FrameType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=16)),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('initial_observation_time', models.DateTimeField()),
                ('sex', models.CharField(choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female')], default='U', max_length=1)),
                ('stage', models.CharField(choices=[('U', 'Unknown'), ('JU', 'Juvenile'), ('AD', 'Adult')], default='U', max_length=2)),
                ('length', models.IntegerField(null=True, help_text='centimeters')),
                ('duration', models.PositiveIntegerField()),
                ('animal', models.ForeignKey(to='bruv.Animal')),
                ('behavior', models.ForeignKey(null=True, to='bruv.AnimalBehavior')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObservationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=6)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=6)),
                ('drop_time', models.DateTimeField()),
                ('collection_time', models.DateTimeField(null=True, blank=True)),
                ('tide_state', models.CharField(max_length=16)),
                ('visibility', models.CharField(choices=[('11', '11'), ('8', '8'), ('12', '12'), ('9', '9'), ('10', '10'), ('4', '4'), ('3', '3'), ('2', '2'), ('14', '14'), ('6', '6'), ('>15', '>15'), ('15', '15'), ('7', '7'), ('1', '1'), ('13', '13'), ('5', '5')], max_length=3)),
                ('depth', models.FloatField(null=True)),
                ('bait', models.CharField(max_length=16, help_text='1kg')),
                ('bait_oiled', models.BooleanField(default=False, help_text='20ml menhaden oil')),
                ('equipment', models.ForeignKey(to='bruv.Equipment')),
                ('reef', models.ForeignKey(null=True, to='habitat.Reef')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
            model_name='equipment',
            name='frame_type',
            field=models.ForeignKey(to='bruv.FrameType'),
        ),
        migrations.AddField(
            model_name='equipment',
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
