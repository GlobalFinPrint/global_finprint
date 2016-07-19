import openpyxl
import os
from datetime import datetime
import logging

from django.core.management.base import BaseCommand, CommandError

import global_finprint.core.management.commands.import_common as ic

logger = logging.getLogger('scripts')

def import_file(in_file):
    'Trip, Set, Environment, Observation'
    wb = openpyxl.load_workbook(in_file)

    import_trip_data(wb['Trip'])
    import_set_data(wb['Set'])

    # Environment
    # trip_code, set_code, date, drop_haul, temp, salinity...

    # Observation
    # trip_code, set_code, date, time...

def import_trip_data(sheet):
    headers = get_header_map(sheet.rows[0])
    get_cell = get_cell_by_name_extractor(headers)
    for row in sheet.rows[1:]:
        trip_code = get_cell(row, 'code').value
        if trip_code:
            location_name = get_cell(row, 'location').value
            start_date = get_date_from_cell(get_cell(row, 'start_date'))
            end_date = get_date_from_cell(get_cell(row, 'end_date'))
            investigator = get_cell(row, 'investigator').value
            collaborator = get_cell(row, 'collaborator').value
            boat = get_cell(row, 'boat').value

            ic.import_trip(
                trip_code,
                location_name,
                start_date,
                end_date,
                investigator,
                collaborator,
                boat
            )

def import_set_data(sheet):
    headers = get_header_map(sheet.rows[0])
    get_cell = get_cell_by_name_extractor(headers)
    for row in sheet.rows[1:]:
        set_code = get_cell(row, 'set_code').value
        if set_code:
            trip_code = get_cell(row, 'trip_code').value
            set_date = get_date_from_cell(get_cell(row, 'date'))
            latitude = get_cell(row, 'latitude').value
            longitude = get_cell(row, 'longitude').value
            try:
                depth_cell = get_cell(row, 'depth')
                depth = get_float_from_cell(depth_cell)
            except ValueError:
                logging.error('Bad depth value "%s"', depth_cell.value)
                logging.error('Set "%s" not created', set_code)
                continue
            drop_time = get_time_from_cell(get_cell(row, 'drop_time'))
            haul_time = get_time_from_cell(get_cell(row, 'haul_time'))
            site_name = get_cell(row, 'site').value
            reef_name = get_cell(row, 'reef').value
            habitat_type = get_cell(row, 'habitat').value
            equipment_str = get_cell(row, 'equipment').value
            bait_str = get_cell(row, 'bait').value
            visibility = get_cell(row, 'visibility').value
            video = get_cell(row, 'video').value
            comment = get_cell(row, 'comment').value

            ic.import_set(
                set_code,
                trip_code,
                set_date,
                latitude,
                longitude,
                depth,
                drop_time,
                haul_time,
                site_name,
                reef_name,
                habitat_type,
                equipment_str,
                bait_str,
                visibility,
                video,
                comment
            )                

def import_environment_data(sheet):
    headers = get_header_map(sheet.rows[0])
    get_cell = get_cell_by_name_extractor(headers)
    for row in sheet.rows[1:]:
        trip_code = get_cell(row, 'trip_code').value
        if trip_code:
            set_code = get_cell(row, 'set_code').value
            reading_date = get_date_from_cell(row, 'date').value
            drop_haul = get_cell(row, 'drop_haul').value
            temp = get_cell(row, 'temp').value
            salinity = get_cell(row, 'salinity').value
            conductivity = get_cell(row, 'conductivity').value
            dissolved_oxygen = get_cell(row, 'dissolved_oxygen').value

def get_cell_by_name_extractor(headers):
    extractor_func = lambda row, column_name: row[headers[column_name]]
    return extractor_func

def get_header_map(header_row):
    result = {}
    for idx, header in enumerate(header_row):
        if header.value:
            result[header.value] = idx
    return result

def get_float_from_cell(cell):
    result = None
    if isinstance(cell.value, str):
        result = float(cell.value)
    else:
        result = cell.value
    return result

def get_date_from_cell(cell):
    if cell.number_format == 'General':
        return datetime.strptime(cell.value, '%d/%m/%Y')
    else:
        return cell.value
    
def get_time_from_cell(cell):
    if cell.number_format == 'General':
        return datetime.strptime(cell.value, '%H:%M:%S %p').time()
    else:
        return cell.value

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('in_file', type=str)

    def handle(self, *args, **options):
        import_file(options['in_file'])
