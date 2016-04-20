from django.core.management.base import BaseCommand
from django.db import connection
from glob import glob


class Command(BaseCommand):
    help = 'Creates DB views'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            views = glob('database/create_v_*.sql')
            for view in views:
                cursor.execute(open(view, 'r').read())
            print('{0} views created successfully'.format(len(views)))
