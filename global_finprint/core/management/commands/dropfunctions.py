from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Drops DB functions'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(open('database/drop_functions.sql', 'r').read())
        print('Functions dropped')
