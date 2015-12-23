# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0001_initial'),
        ('bruv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='video',
            field=models.OneToOneField(to='annotation.Video', related_name='set', null=True),
        ),
    ]
