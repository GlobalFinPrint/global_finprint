from __future__ import unicode_literals

import config.current_user
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annotation', '0018_migrate_obs_to_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observationimage',
            name='observation',
        ),
        migrations.RemoveField(
            model_name='observationimage',
            name='user',
        ),
        migrations.RemoveField(
            model_name='observationimage',
            name='video',
        ),
        migrations.RemoveField(
            model_name='siteimage',
            name='user',
        ),
        migrations.RemoveField(
            model_name='siteimage',
            name='video',
        ),
        migrations.RemoveField(
            model_name='animalobservation',
            name='behaviors',
        ),
        migrations.RemoveField(
            model_name='animalobservation',
            name='features',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='extent',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='initial_observation_time',
        ),
        migrations.AlterField(
            model_name='animalobservation',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unknown')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='observation',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='observation',
            name='type',
            field=models.CharField(choices=[('I', 'Of interest'), ('A', 'Animal')], default='I', max_length=1),
        ),
        migrations.DeleteModel(
            name='AnimalBehavior',
        ),
        migrations.DeleteModel(
            name='ObservationFeature',
        ),
        migrations.DeleteModel(
            name='ObservationImage',
        ),
        migrations.DeleteModel(
            name='SiteImage',
        ),
    ]

