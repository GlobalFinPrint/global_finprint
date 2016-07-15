import openpyxl
import click
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from global_finprint.trip.models import Source, Trip
from global_finprint.core.models import Team
from global_finprint.habitat.models import Location
from global_finprint.bruv.models import Set

def import_file(in_file):
    'Trip, Set, Environment, Observation'
    wb = openpyxl.load_workbook(in_file)

    # Trip
    import_trip_data(wb['Trip'])

    # Set
    # trip_code, set_code, date, latitude, longitude, depth, drop_time, haul_time...
    import_set_data(wb['Set'])

    # Environment
    # trip_code, set_code, date, drop_haul, temp, salinity...

    # Observation
    # trip_code, set_code, date, time...

def import_trip_data(sheet):
    headers = get_header_map(sheet.rows[0])
    get_cell = get_cell_by_name_extractor(headers)
    import_user = User.objects.filter(username='GFAdmin').first()
    for row in sheet.rows[1:]:
        trip_code = get_cell(row, 'code').value
        if trip_code:
            trip = Trip.objects.filter(code='FP_2015_BS_21').first()
            if not trip:
                location_name = get_cell(row, 'location').value
                location = Location.objects.filter(name=location_name).first()
                start_date = get_date_from_cell(get_cell(row, 'start_date'))
                end_date = get_date_from_cell(get_cell(row, 'end_date'))
                investigator = get_cell(row, 'investigator').value
                collaborator = get_cell(row, 'collaborator').value
                boat = get_cell(row, 'boat').value
                trip = Trip(
                    code=trip_code,
                    team=Team.objects.first(), # need to grab correct one
                    source=Source.objects.first(), # need to grab correct one
                    location=location,
                    boat=boat,
                    start_date=start_date,
                    end_date=end_date,
                    user=import_user
                )
                trip.save()

def import_set_data(sheet):
    headers = get_header_map(sheet.rows[0])
    get_cell = get_cell_by_name_extractor(headers)
    import_user = User.objects.filter(username='GFAdmin').first()
    for row in sheet.rows[1:]:
        set_code = get_cell(row, 'set_code').value
        if set_code:
            pass

def get_cell_by_name_extractor(headers):
    extractor_func = lambda row, column_name: row[headers[column_name]]
    return extractor_func

def get_header_map(header_row):
    result = {}
    for idx, header in enumerate(header_row):
        if header.value:
            result[header.value] = idx
    return result

def get_date_from_cell(cell):
    if cell.number_format == 'General':
        return datetime.strptime(cell.value, '%d/%m/%Y')
    else:
        return cell.value

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('in_file', type=str)

    def handle(self, *args, **options):
        print(args)
        import_file(options['in_file'])
