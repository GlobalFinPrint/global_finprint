# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import config.current_user
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentMeasure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('measurement_time', models.DateTimeField()),
                ('water_temperature', models.IntegerField(help_text='C', null=True)),
                ('salinity', models.DecimalField(decimal_places=2, max_digits=4, help_text='ppt', null=True)),
                ('conductivity', models.DecimalField(decimal_places=2, max_digits=4, help_text='S/m', null=True)),
                ('dissolved_oxygen', models.DecimalField(decimal_places=1, max_digits=3, help_text='%', null=True)),
                ('current_flow', models.DecimalField(decimal_places=2, max_digits=5, help_text='m/s', null=True)),
                ('current_direction', models.CharField(max_length=2, help_text='compass direction', choices=[('NW', 'Northwest'), ('S', 'South'), ('SE', 'Southeast'), ('NE', 'Northeast'), ('E', 'East'), ('W', 'West'), ('SW', 'Southwest'), ('N', 'North')], null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('camera', models.CharField(max_length=16)),
                ('stereo', models.BooleanField(default=False)),
                ('bait_container', models.CharField(max_length=1, default='C', choices=[('B', 'Bag'), ('C', 'Cage')])),
                ('arm_length', models.PositiveIntegerField(help_text='centimeters')),
                ('camera_height', models.PositiveIntegerField(help_text='centimeters')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FrameType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=16)),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('initial_observation_time', models.DateTimeField()),
                ('sex', models.CharField(max_length=1, default='U', choices=[('F', 'Female'), ('U', 'Unknown'), ('M', 'Male')])),
                ('stage', models.CharField(max_length=2, default='U', choices=[('AD', 'Adult'), ('JU', 'Juvenile'), ('U', 'Unknown')])),
                ('length', models.IntegerField(help_text='centimeters', null=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('drop_time', models.DateTimeField()),
                ('collection_time', models.DateTimeField(null=True, blank=True)),
                ('tide_state', models.CharField(max_length=16)),
                ('visibility', models.CharField(max_length=3, choices=[('14', '14'), ('15', '15'), ('13', '13'), ('12', '12'), ('9', '9'), ('8', '8'), ('5', '5'), ('>15', '>15'), ('7', '7'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1'), ('10', '10'), ('6', '6'), ('11', '11')])),
                ('depth', models.FloatField(null=True)),
                ('bait', models.CharField(max_length=16, help_text='1kg')),
                ('bait_oiled', models.BooleanField(help_text='20ml menhaden oil', default=False)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
