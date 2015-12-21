# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings
import config.current_user


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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=16, help_text='1kg')),
                ('type', models.CharField(choices=[('WHL', 'Whole'), ('CRS', 'Crushed'), ('CHP', 'Chopped')], max_length=3)),
                ('oiled', models.BooleanField(default=False, help_text='20ml menhaden oil')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnvironmentMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('water_temperature', models.DecimalField(max_digits=4, null=True, decimal_places=1, help_text='C', blank=True)),
                ('salinity', models.DecimalField(max_digits=4, null=True, decimal_places=2, help_text='ppt', blank=True)),
                ('conductivity', models.DecimalField(max_digits=4, null=True, decimal_places=2, help_text='S/m', blank=True)),
                ('dissolved_oxygen', models.DecimalField(max_digits=3, null=True, decimal_places=1, help_text='%', blank=True)),
                ('current_flow', models.DecimalField(max_digits=5, null=True, decimal_places=2, help_text='m/s', blank=True)),
                ('current_direction', models.CharField(choices=[('N', 'North'), ('SW', 'Southwest'), ('NW', 'Northwest'), ('SE', 'Southeast'), ('S', 'South'), ('W', 'West'), ('NE', 'Northeast'), ('E', 'East')], max_length=2, null=True, help_text='compass direction', blank=True)),
                ('tide_state', models.CharField(choices=[('F', 'Flood'), ('S2F', 'Slack to Flood'), ('E', 'Ebb'), ('S2E', 'Slack to Ebb'), ('S', 'Slack')], max_length=3, null=True, blank=True)),
                ('estimated_wind_speed', models.IntegerField(null=True, blank=True)),
                ('wind_direction', models.CharField(choices=[('N', 'North'), ('SW', 'Southwest'), ('NW', 'Northwest'), ('SE', 'Southeast'), ('S', 'South'), ('W', 'West'), ('NE', 'Northeast'), ('E', 'East')], max_length=2, null=True, help_text='compass direction', blank=True)),
                ('cloud_cover', models.IntegerField(null=True, help_text='%', blank=True)),
                ('surface_chop', models.CharField(choices=[('M', 'Medium'), ('L', 'Light'), ('H', 'Heavy')], max_length=1, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
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
                ('camera', models.CharField(max_length=16)),
                ('stereo', models.BooleanField(default=False)),
                ('bait_container', models.CharField(choices=[('C', 'Cage'), ('B', 'Bag')], max_length=1, default='C')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('set_date', models.DateField()),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=6)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=6)),
                ('drop_time', models.TimeField()),
                ('haul_time', models.TimeField()),
                ('visibility', models.CharField(choices=[('14', '14'), ('4', '4'), ('12', '12'), ('10', '10'), ('>15', '>15'), ('8', '8'), ('3', '3'), ('2', '2'), ('13', '13'), ('9', '9'), ('6', '6'), ('11', '11'), ('7', '7'), ('5', '5'), ('1', '1'), ('15', '15')], max_length=3)),
                ('depth', models.FloatField(null=True, help_text='m')),
                ('comments', models.CharField(max_length=255, null=True, blank=True)),
                ('bait', models.OneToOneField(to='bruv.Bait', null=True, related_name='bait_parent_set')),
                ('drop_measure', models.OneToOneField(to='bruv.EnvironmentMeasure', null=True, related_name='drop_parent_set')),
                ('equipment', models.ForeignKey(to='bruv.Equipment')),
                ('haul_measure', models.OneToOneField(to='bruv.EnvironmentMeasure', null=True, related_name='haul_parent_set')),
                ('reef', models.ForeignKey(to='habitat.Reef')),
                ('trip', models.ForeignKey(to='trip.Trip')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
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
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user),
        ),
    ]
