import logging
import functools

import django.contrib.auth.models as djam
import global_finprint.trip.models as gftm
import global_finprint.core.models as gfcm
import global_finprint.habitat.models as gfhm
import global_finprint.bruv.models as gfbm
from django.contrib.gis.geos import GEOSGeometry

FRAME_FIELD_LENGTH = 32
CAMERA_FIELD_LENGTH = 32

logger = logging.getLogger('scripts')

class DataError(Exception):
    pass

@functools.lru_cache()
def get_bait_type_map():
    return  make_choices_reverse_map(gfbm.BAIT_TYPE_CHOICES)

@functools.lru_cache()
def get_tide_state_map():
    return  make_choices_reverse_map(gfbm.TIDE_CHOICES)

@functools.lru_cache()
def get_surface_chop_map():
    return  make_choices_reverse_map(gfbm.SURFACE_CHOP_CHOICES)

def make_choices_reverse_map(choices_set):
    result = {}
    for abrev, verbose in choices_set:
        result[verbose.lower()] = abrev
    return result

@functools.lru_cache()
def get_import_user():
    return djam.User.objects.filter(username='GFAdmin').first()

def import_trip(
        trip_code,
        location_name,
        start_date,
        end_date,
        investigator,
        collaborator,
        boat,
):
    try:
        logger.info('Working on trip "%s"', trip_code)
        trip = gftm.Trip.objects.filter(code=trip_code).first()
        if not trip:
            location = gfhm.Location.objects.filter(name=location_name).first()
            lead_candidates = djam.User.objects.filter(last_name=investigator)
            validate_data(
                len(lead_candidates) > 0,
                'No investigator with last name {}'.format(investigator))
            validate_data(
                len(lead_candidates) < 2,
                'More than one investigator with last name {}'.format(investigator))

            lead = gfcm.FinprintUser.objects.filter(user=lead_candidates[0]).first()
            validate_data(lead, 'No FinprintUser associated with User "{}"'.format(investigator))

            team=gfcm.Team.objects.filter(
                lead=lead,
                sampler_collaborator=collaborator).first()
            validate_data(team, 'No such team: {} - {}'.format(investigator, collaborator))

            source = gftm.Source.objects.filter(code=trip_code[:2]).first()

            trip = gftm.Trip(
                code=trip_code,
                team=team,
                source=source,
                location=location,
                boat=boat,
                start_date=start_date,
                end_date=end_date,
                user=get_import_user()
            )
            trip.save()
            logger.info('Created trip "%s"', trip_code)
        else:
            logger.warning('Trip "%s" already exists. Ignoring.', trip_code)
    except DataError:
        logger.error('Trip "%s" not created.', trip_code)

def import_set(
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
):
    try:
        logger.info('Working on set "%s"', set_code)
        trip = gftm.Trip.objects.filter(code=trip_code).first()
        validate_data(trip, 'references non-existent trip "{}"'.format(trip_code))
        the_set = gfbm.Set.objects.filter(code=set_code, trip=trip).first()
        if not the_set:
            validate_data(drop_time < haul_time, 'Drop time must be before haul time.')
            reef_habitat = get_reef_habitat(site_name, reef_name, habitat_type)
            equipment = parse_equipment_string(equipment_str)
            bait = parse_bait_string(bait_str)
            if not visibility:
                visibility = '0'

            set = gfbm.Set(
                code=set_code,
                set_date=set_date,
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
                user=get_import_user()
            )
            set.save()
            logger.info('Created set "%s"', set_code)
        else:
            logger.warning('Set "%s" already exists, ignoring.', set_code)
    except DataError:
        logger.error('Set "%s" not created.', set_code)
    
def import_environment_measure(
        trip_code,
        set_code,
        reading_date,
        is_drop,
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
):
    measure_type = 'drop' if is_drop else 'haul'
    try:
        logger.info('Trying to add %s data for set "%s" on trip "%s"', measure_type, set_code, trip_code)

        the_trip = gftm.Trip.objects.filter(code=trip_code).first()
        validate_data(the_trip, 'Trip "{}" not found when trying to import environment measure.'.format(trip_code))

        the_set = gfbm.Set.objects.filter(code=set_code, trip=the_trip).first()
        validate_data(the_set, 'Set "{}" not found when trying to import environment measure.'.format(set_code))

        # Only add if data doesn't already exist
        if (is_drop and not the_set.drop_measure) or (not is_drop and not the_set.haul_measure):
            # normalize strings (all may be None)
            if current_direction:
                current_direction = current_direction.upper()
            if tide_state:
                try:
                    tide_state = get_tide_state_map()[tide_state.lower()]
                except KeyError:
                    valdiate_data(
                        False,
                        'Bad tide_state "%s" for set "%s" of trip "%s"', tide_state, set_code, trip_code
                    )
            if wind_direction:
                wind_direction = wind_direction.upper()
            if surface_chop:
                try:
                    surface_chop = get_surface_chop_map()[surface_chop.lower()]
                except KeyError:
                    valdiate_data(
                        False,
                        'Bad tide_state "%s" for set "%s" of trip "%s"', tide_state, set_code, trip_code
                    )

            enviro_measure = gfbm.EnvironmentMeasure(
                water_temperature=temp,
                salinity=salinity,
                conductivity=conductivity,
                dissolved_oxygen=dissolved_oxygen,
                current_flow=current_flow,
                current_direction=current_direction,
                tide_state=tide_state,
                estimated_wind_speed=wind_speed,
                wind_direction=wind_direction,
                cloud_cover=cloud_cover,
                surface_chop=surface_chop,
                user=get_import_user()
            )
            enviro_measure.save()
            if is_drop:
                the_set.drop_measure = enviro_measure
            else:
                the_set.haul_measure = enviro_measure
            the_set.save()
            logger.info('%s data added.', measure_type)
        else:
            logger.warning(
                'Set "%s" of trip "%s" already has %s data specified.',
                set_code,
                trip_code,
                measure_type
            )
    except DataError:
        logger.error('Failed while adding %s data for set "%s" on trip "%s"', measure_type, set_code, trip_code)

def get_reef_habitat(site_name, reef_name, habitat_type):
    site = gfhm.Site.objects.filter(name=site_name).first()
    validate_data(site, 'Site "{}" not found'.format(site_name))

    reef = gfhm.Reef.objects.filter(name=reef_name, site=site).first()
    validate_data(reef, 'Reef "{}" not found'.format(reef_name))

    reef_type = gfhm.ReefType.objects.filter(type=habitat_type).first()
    validate_data(reef_type, 'Unknown reef type: {}'.format(reef_type))

    return gfhm.ReefHabitat.get_or_create(reef, reef_type)

def parse_equipment_string(equipment_str):
    equip_array = equipment_str.split('/')
    validate_data(
        len(equip_array) == 2,
        'Unexpected equipment string: "{}"'.format(equipment_str))
    frame_str = equip_array[0][:FRAME_FIELD_LENGTH]
    camera_str = equip_array[1][:CAMERA_FIELD_LENGTH]
    frame = gfbm.FrameType.objects.filter(type__iexact=frame_str).first()
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
            user=get_import_user())
        equipment.save()
    return equipment

def parse_bait_string(bait_str):
    bait = None
    if bait_str:
        bait_array = bait_str.split(',')
        validate_data(len(bait_array) == 2, 'Unexpected bait string: {}'.format(bait_str))
        bait_description = bait_array[0].strip()
        bait_type_str = bait_array[1].strip()
        try:
            bait_type = get_bait_type_map()[bait_type_str.lower()]
        except KeyError:
            validate_data(False, 'Unknown bait type: {}'.format(bait_type_str))
        bait = gfbm.Bait.objects.filter(
            description=bait_description,
            type=bait_type).first()
        if not bait:
            bait = gfbm.Bait(
                description=bait_description,
                type=bait_type,
                user=get_import_user())
            bait.save()
    return bait

def validate_data(predicate, error_msg):
    if not predicate:
        logger.error(error_msg)
        raise DataError()
