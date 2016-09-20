from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bruv', '0017_auto_20160920_1653'),
    ]

    operations = [
        migrations.RunSQL('''
            UPDATE bruv_set
            SET haul_date =
            (
              SELECT CASE WHEN haul_time < drop_time
                THEN s.set_date + INTERVAL '1 day'
                     ELSE s.set_date
                     END
              FROM bruv_set s
              WHERE s.id = bruv_set.id
            )
            WHERE haul_date IS NULL;
    '''),
    ]
