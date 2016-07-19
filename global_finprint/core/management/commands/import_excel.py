import openpyxl
import os
from datetime import datetime
import logging

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from global_finprint.trip.models import Source, Trip
from global_finprint.core.models import Team, FinprintUser
from global_finprint.habitat.models import Location, Site, ReefHabitat, Reef, ReefType
import global_finprint.bruv.models as gfbm
from django.contrib.gis.geos import GEOSGeometry

logger = logging.getLogger('scripts')
FRAME_FIELD_LENGTH = 32
CAMERA_FIELD_LENGTH = 32

class DataError(Exception):
    pass

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
    import_user = User.objects.filter(username='GFAdmin').first()
    for row in sheet.rows[1:]:
        trip_code = get_cell(row, 'code').value
        if trip_code:
            try:
                logger.info('Working on trip "%s"', trip_code)
                trip = Trip.objects.filter(code=trip_code).first()
                if not trip:
                    location_name = get_cell(row, 'location').value
                    location = Location.objects.filter(name=location_name).first()
                    start_date = get_date_from_cell(get_cell(row, 'start_date'))
                    end_date = get_date_from_cell(get_cell(row, 'end_date'))

                    investigator = get_cell(row, 'investigator').value
                    collaborator = get_cell(row, 'collaborator').value
                    lead_candidates = User.objects.filter(last_name=investigator)
                    validate_data(
                        len(lead_candidates) > 0,
                        'No investigator with last name {}'.format(investigator))
                    validate_data(
                        len(lead_candidates) < 2,
                        'More than one investigator with last name {}'.format(investigator))
                    lead = FinprintUser.objects.filter(user=lead_candidates[0]).first()
                    validate_data(lead, 'No FinprintUser associated with User "{}"'.format(investigator))
                    team=Team.objects.filter(
                        lead=lead,
                        sampler_collaborator=collaborator).first()
                    validate_data(team, 'No such team: {} - {}'.format(investigator, collaborator))

                    source = Source.objects.filter(code=trip_code[:2]).first()
                    boat = get_cell(row, 'boat').value

                    trip = Trip(
                        code=trip_code,
                        team=team,
                        source=source,
                        location=location,
                        boat=boat,
                        start_date=start_date,
                        end_date=end_date,
                        user=import_user
                    )
                    trip.save()
                    logger.info('Created trip "%s"', trip_code)
                else:
                    logger.warning('Trip "%s" already exists. Ignoring.', trip_code)
            except DataError:
                logger.error('Trip "%s" not created.', trip_code)

def import_set_data(sheet):
    headers = get_header_map(sheet.rows[0])
    get_cell = get_cell_by_name_extractor(headers)
    import_user = User.objects.filter(username='GFAdmin').first()
    bait_map = get_bait_type_map()
    for row in sheet.rows[1:]:
            set_code = get_cell(row, 'set_code').value
            if set_code:
                try:
                    logger.info('Working on set "%s"', set_code)
                    trip_code = get_cell(row, 'trip_code').value
                    trip = Trip.objects.filter(code=trip_code).first()
                    validate_data(trip, 'references non-existent trip "{}"'.format(trip_code))
                    set = gfbm.Set.objects.filter(code=set_code, trip=trip).first()
                    if not set:
                        date = get_date_from_cell(get_cell(row, 'date'))
                        latitude = get_cell(row, 'latitude').value
                        longitude = get_cell(row, 'longitude').value
                        try:
                            depth_cell = get_cell(row, 'depth')
                            depth = get_float_from_cell(depth_cell)
                        except ValueError:
                            validate_data(False, 'Bad depth value "{}"'.format(depth_cell.value))

                        drop_time = get_time_from_cell(get_cell(row, 'drop_time'))
                        haul_time = get_time_from_cell(get_cell(row, 'haul_time'))
                        validate_data(drop_time < haul_time, 'Drop time must be before haul time.')

                        site_name = get_cell(row, 'site').value
                        site = Site.objects.filter(name=site_name).first()
                        validate_data(site, 'Site "{}" not found'.format(site_name))

                        reef_name = get_cell(row, 'reef').value
                        reef = Reef.objects.filter(name=reef_name, site=site).first()
                        validate_data(reef, 'Reef "{}" not found'.format(reef_name))

                        habitat_type = get_cell(row, 'habitat').value
                        reef_type = ReefType.objects.filter(type=habitat_type).first()
                        validate_data(reef_type, 'Unknown reef type: {}'.format(reef_type))

                        reef_habitat = ReefHabitat.get_or_create(reef, reef_type)

                        equipment_str = get_cell(row, 'equipment').value
                        equip_array = equipment_str.split('/')
                        validate_data(
                            len(equip_array) == 2,
                            'Unexpected equipment string: "{}"'.format(equipment_str))
                        frame_str = equip_array[0][:FRAME_FIELD_LENGTH]
                        camera_str = equip_array[1][:CAMERA_FIELD_LENGTH]
                        frame = gfbm.FrameType.objects.filter(type__iexact=frame_str)
                        if not frame:
                            frame = gfbm.FrameType(type=frame_str)
                            frame.save()
                        equipment = gfbm.Equipment.objects.filter(
                            camera=camera_str,
                            frame_type=frame).first()
                        if not equipment:
                            equipment = gfbm.Equipment(
                                camera=camera_str,
                                frame_type=frame,
                                arm_length=1,
                                camera_height=1,
                                user=import_user)
                            equipment.save()

                        bait = None
                        bait_str = get_cell(row, 'bait').value
                        if bait_str:
                            bait_array = bait_str.split(',')
                            validate_data(len(bait_array) == 2, 'Unexpected bait string: {}'.format(bait_str))
                            bait_description = bait_array[0].strip()
                            bait_type_str = bait_array[1].strip()
                            try:
                                bait_type = bait_map[bait_type_str.lower()]
                            except KeyError:
                                validate_data(False, 'Unknown bait type: {}'.format(bait_type_str))
                            bait = gfbm.Bait.objects.filter(
                                description=bait_description,
                                type=bait_type).first()
                            if not bait:
                                bait = gfbm.Bait(
                                    description=bait_description,
                                    type=bait_type,
                                    user=import_user)
                                bait.save()

                        visibility = get_cell(row, 'visibility').value
                        if not visibility:
                            visibility = '0'
                        video = get_cell(row, 'video').value
                        comment = get_cell(row, 'comment').value
                        set = gfbm.Set(
                            code=set_code,
                            set_date=date,
                            latitude=latitude,
                            longitude=longitude,
                            drop_time=drop_time,
                            haul_time=haul_time,
                            visibility=visibility,
                            depth=depth,
                            comments=comment,
                            bait=bait,
                            equipment=equipment,
                            reef_habitat=reef_habitat,
                            trip=trip,
                            user=import_user
                        )
                        set.save()
                        logger.info('Created set "%s"', set_code)
                    else:
                        logger.warning('Set "%s" already exists ignoring.', set_code)
                except DataError:
                    logger.error('Set "%s" not created.', set_code)

def validate_data(predicate, error_msg):
    if not predicate:
        logger.error(error_msg)
        raise DataError()

def get_cell_by_name_extractor(headers):
    extractor_func = lambda row, column_name: row[headers[column_name]]
    return extractor_func

def get_bait_type_map():
    result = {}
    for abrev, verbose in gfbm.BAIT_TYPE_CHOICES:
        result[verbose.lower()] = abrev
    return result

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
