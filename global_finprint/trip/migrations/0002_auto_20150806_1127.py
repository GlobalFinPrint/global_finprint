# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reef',
            name='site',
            field=models.ForeignKey(to='trip.Site', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='site',
            name='location',
            field=models.ForeignKey(to='trip.Location', default=1),
            preserve_default=False,
        ),
    ]
