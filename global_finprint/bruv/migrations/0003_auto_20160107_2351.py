# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0002_add_video_to_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='drop_id',
            field=models.CharField(max_length=32, default='FP_TEST'),
            preserve_default=False,
        ),
    ]
