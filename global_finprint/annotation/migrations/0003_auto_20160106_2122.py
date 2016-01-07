# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0002_auto_20160104_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotator',
            name='token',
            field=models.CharField(null=True, max_length=32),
        ),
        migrations.AddField(
            model_name='lead',
            name='token',
            field=models.CharField(null=True, max_length=32),
        ),
        migrations.AlterField(
                model_name='annotator',
                name='user',
                field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
                model_name='lead',
                name='user',
                field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
