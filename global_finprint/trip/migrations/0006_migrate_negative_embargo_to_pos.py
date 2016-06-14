from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('trip', '0005_auto_20160419_1822'),
    ]

    operations = [
        migrations.RunSQL('''
          update trip_source
            set data_embargo_length = 0
            where data_embargo_length < 0;
        '''),
    ]
