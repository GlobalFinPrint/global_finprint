# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import config.current_user
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
            name='Bait',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=16, help_text='1kg')),
                ('type', models.CharField(max_length=3, choices=[('WHL', 'Whole'), ('CHP', 'Chopped'), ('CRS', 'Crushed')])),
                ('oiled', models.BooleanField(default=False, help_text='20ml menhaden oil')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnvironmentMeasure',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('water_temperature', models.DecimalField(help_text='C', blank=True, null=True, max_digits=4, decimal_places=1)),
                ('salinity', models.DecimalField(help_text='ppt', blank=True, null=True, max_digits=4, decimal_places=2)),
                ('conductivity', models.DecimalField(help_text='S/m', blank=True, null=True, max_digits=4, decimal_places=2)),
                ('dissolved_oxygen', models.DecimalField(help_text='%', blank=True, null=True, max_digits=3, decimal_places=1)),
                ('current_flow', models.DecimalField(help_text='m/s', blank=True, null=True, max_digits=5, decimal_places=2)),
                ('current_direction', models.CharField(blank=True, max_length=2, help_text='compass direction', choices=[('W', 'West'), ('E', 'East'), ('NW', 'Northwest'), ('N', 'North'), ('S', 'South'), ('SW', 'Southwest'), ('SE', 'Southeast'), ('NE', 'Northeast')], null=True)),
                ('tide_state', models.CharField(blank=True, max_length=3, null=True, choices=[('F', 'Flood'), ('S2F', 'Slack to Flood'), ('S', 'Slack'), ('E', 'Ebb'), ('S2E', 'Slack to Ebb')])),
                ('estimated_wind_speed', models.IntegerField(null=True, blank=True)),
                ('wind_direction', models.CharField(blank=True, max_length=2, help_text='compass direction', choices=[('W', 'West'), ('E', 'East'), ('NW', 'Northwest'), ('N', 'North'), ('S', 'South'), ('SW', 'Southwest'), ('SE', 'Southeast'), ('NE', 'Northeast')], null=True)),
                ('cloud_cover', models.IntegerField(help_text='%', blank=True, null=True)),
                ('surface_chop', models.CharField(blank=True, max_length=1, null=True, choices=[('L', 'Light'), ('M', 'Medium'), ('H', 'Heavy')])),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('camera', models.CharField(max_length=16)),
                ('stereo', models.BooleanField(default=False)),
                ('bait_container', models.CharField(default='C', choices=[('C', 'Cage'), ('B', 'Bag')], max_length=1)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=16)),
                ('image', models.ImageField(upload_to='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('drop_id', models.CharField(max_length=32)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('set_date', models.DateField()),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('drop_time', models.TimeField()),
                ('haul_time', models.TimeField()),
                ('visibility', models.CharField(max_length=3, choices=[('14', '14'), ('9', '9'), ('11', '11'), ('8', '8'), ('7', '7'), ('5', '5'), ('>15', '>15'), ('4', '4'), ('12', '12'), ('15', '15'), ('3', '3'), ('2', '2'), ('1', '1'), ('10', '10'), ('13', '13'), ('6', '6')])),
                ('depth', models.FloatField(help_text='m', null=True)),
                ('comments', models.CharField(max_length=255, null=True, blank=True)),
                ('bait', models.OneToOneField(null=True, to='bruv.Bait', related_name='bait_parent_set')),
                ('drop_measure', models.OneToOneField(null=True, to='bruv.EnvironmentMeasure', related_name='drop_parent_set')),
                ('equipment', models.ForeignKey(to='bruv.Equipment')),
                ('haul_measure', models.OneToOneField(null=True, to='bruv.EnvironmentMeasure', related_name='haul_parent_set')),
                ('reef_habitat', models.ForeignKey(to='habitat.ReefHabitat')),
                ('trip', models.ForeignKey(to='trip.Trip')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
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
    ]
