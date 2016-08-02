"""
import_excel
Author: Tyler Sellon

Adds "import_excel" command, accessible through manage.py.

Takes a single excel workbook and imports the data.

File format is specified here:
https://www.dropbox.com/s/5yy0bb4mxbm0mdj/data_collection_standards.xlsx?dl=0
"""
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
    import_environment_data(wb['Environment'])
    import_observation_data(wb['Observation'])

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
            reading_date = get_date_from_cell(get_cell(row, 'date'))
            drop_haul = get_cell(row, 'drop_haul').value
            temp = get_float_from_cell(get_cell(row, 'temp'))
            salinity = get_float_from_cell(get_cell(row, 'salinity'))
            conductivity = get_float_from_cell(get_cell(row, 'conductivity'))
            dissolved_oxygen = get_float_from_cell(get_cell(row, 'dissolved_oxygen'))
            current_flow = get_float_from_cell(get_cell(row, 'current_flow'))
            current_direction = get_cell(row, 'current_direction').value
            tide_state = get_cell(row, 'tide_state').value
            wind_speed = get_float_from_cell(get_cell(row, 'wind_speed'))
            wind_direction = get_cell(row, 'wind_direction').value
            cloud_cover = get_float_from_cell(get_cell(row, 'cloud_cover'))
            surface_chop = get_cell(row, 'surface_chop').value

            ic.import_environment_measure(
                trip_code,
                set_code,
                reading_date,
                drop_haul.lower() == 'drop',
                temp,
                salinity,
                conductivity,
                dissolved_oxygen,
                current_flow,
                current_direction,
                tide_state,
                wind_speed,
                wind_direction,
                cloud_cover,
                surface_chop
            )

def import_observation_data(sheet):
    headers = get_header_map(sheet.rows[0])
    get_cell = get_cell_by_name_extractor(headers)
    for row in sheet.rows[1:]:
        trip_code = get_cell(row, 'trip_code').value
        if trip_code:
            set_code = get_cell(row, 'set_code').value
            obvs_date = get_date_from_cell(get_cell(row, 'date'))
            obvs_time = get_cell(row, 'time').value
            duration = get_cell(row, 'duration').value
            family = get_cell(row, 'family').value
            genus = get_cell(row, 'genus').value
            species = get_cell(row, 'species').value
            behavior = get_cell(row, 'behaviour').value
            sex = get_cell(row, 'sex').value
            stage = get_cell(row, 'stage').value
            length = get_cell(row, 'length').value
            comment = get_cell(row, 'comment').value
            annotator = get_cell(row, 'annotator').value
            annotation_date = get_date_from_cell(get_cell(row, 'date'))

            ic.import_observation(
                trip_code,
                set_code,
                obvs_date,
                obvs_time,
                duration,
                family,
                genus,
                species,
                behavior,
                sex,
                stage,
                length,
                comment,
                annotator,
                annotation_date
            )

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
    help = 'Imports observation data from excel format. Usage: python manage.py import_excel <excel_file>'

    def add_arguments(self, parser):
        parser.add_argument('in_file', type=str)

    def handle(self, *args, **options):
        import_file(options['in_file'])