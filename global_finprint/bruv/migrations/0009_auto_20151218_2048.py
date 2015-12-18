# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import config.current_user
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bruv', '0008_auto_20151209_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bait',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(help_text='1kg', max_length=16)),
                ('type', models.CharField(choices=[('WHL', 'Whole'), ('CRS', 'Crushed'), ('CHP', 'Chopped')], max_length=3)),
                ('oiled', models.BooleanField(help_text='20ml menhaden oil', default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='set',
            name='bait_oiled',
        ),
        migrations.RemoveField(
            model_name='set',
            name='collection_time',
        ),
        migrations.RemoveField(
            model_name='set',
            name='bait'
        ),
        migrations.AddField(
            model_name='set',
            name='bait',
            field=models.OneToOneField(related_name='bait_parent_set', to='bruv.Bait', null=True),
        ),
        migrations.AddField(
            model_name='set',
            name='comments',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='set',
            name='haul_time',
            field=models.TimeField(default=datetime.datetime(2015, 12, 18, 20, 48, 6, 494677, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='set',
            name='set_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 18, 20, 48, 12, 918746, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='animal',
            name='group',
            field=models.CharField(choices=[('S', 'Shark'), ('T', 'Other target'), ('N', 'n/a'), ('G', 'Groupers and jacks'), ('R', 'Ray')], max_length=1),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='cloud_cover',
            field=models.IntegerField(help_text='%', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='conductivity',
            field=models.DecimalField(max_digits=4, help_text='S/m', blank=True, decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(null=True, choices=[('NW', 'Northwest'), ('W', 'West'), ('N', 'North'), ('SE', 'Southeast'), ('NE', 'Northeast'), ('SW', 'Southwest'), ('E', 'East'), ('S', 'South')], help_text='compass direction', blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_flow',
            field=models.DecimalField(max_digits=5, help_text='m/s', blank=True, decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='dissolved_oxygen',
            field=models.DecimalField(max_digits=3, help_text='%', blank=True, decimal_places=1, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='estimated_wind_speed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='salinity',
            field=models.DecimalField(max_digits=4, help_text='ppt', blank=True, decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='surface_chop',
            field=models.CharField(choices=[('L', 'Light'), ('H', 'Heavy'), ('M', 'Medium')], null=True, blank=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='tide_state',
            field=models.CharField(choices=[('S2F', 'Slack to Flood'), ('S2E', 'Slack to Ebb'), ('S', 'Slack'), ('E', 'Ebb'), ('F', 'Flood')], null=True, blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='water_temperature',
            field=models.DecimalField(max_digits=4, help_text='C', blank=True, decimal_places=1, null=True),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='wind_direction',
            field=models.CharField(null=True, choices=[('NW', 'Northwest'), ('W', 'West'), ('N', 'North'), ('SE', 'Southeast'), ('NE', 'Northeast'), ('SW', 'Southwest'), ('E', 'East'), ('S', 'South')], help_text='compass direction', blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('U', 'Unknown'), ('F', 'Female')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(choices=[('U', 'Unknown'), ('JU', 'Juvenile'), ('AD', 'Adult')], default='U', max_length=2),
        ),
        migrations.AlterField(
            model_name='set',
            name='drop_measure',
            field=models.OneToOneField(related_name='drop_parent_set', to='bruv.EnvironmentMeasure', null=True),
        ),
        migrations.AlterField(
            model_name='set',
            name='drop_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='set',
            name='haul_measure',
            field=models.OneToOneField(related_name='haul_parent_set', to='bruv.EnvironmentMeasure', null=True),
        ),
        migrations.AlterField(
            model_name='set',
            name='reef',
            field=models.ForeignKey(to='habitat.Reef', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(choices=[('2', '2'), ('1', '1'), ('10', '10'), ('7', '7'), ('>15', '>15'), ('8', '8'), ('6', '6'), ('5', '5'), ('3', '3'), ('15', '15'), ('13', '13'), ('14', '14'), ('11', '11'), ('12', '12'), ('9', '9'), ('4', '4')], max_length=3),
        ),
    ]
