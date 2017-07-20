from django.core.management.base import BaseCommand
from django.db import connection
from glob import glob


class Command(BaseCommand):
    help = 'Creates DB functions'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            views = glob('database/create_f_*.sql')
            for view in sorted(views):
                print('creating function {}'.format(view))
                cursor.execute(open(view, 'r').read())
            print('{0} funcitons created successfully'.format(len(views)))
