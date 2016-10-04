"""
import_common
Author: Tyler Sellon

Package for common functionality used in Finprint's bulk data importation. All
model related logic should be in here. File parsing should be done in other
modules which call into this package.

Main externally facing API is:
import_trip: create a trip model
import_set: create a set model
import_environment_measure: adds environment data to a set
import_observation: adds an observation to a set

If data already exists, a warning is logged. If data is incomplete or malformed,
an error is logged. In ether case, no error is raised to the caller. If use of
this package spreads to functions beyond basic bulk import commands, we should
add error signaling.
"""
import logging
import functools
import json
from datetime import datetime

import django.contrib.auth.models as djam
import global_finprint.trip.models as gftm
import global_finprint.core.models as gfcm
import global_finprint.habitat.models as gfhm
import global_finprint.bruv.models as gfbm
import global_finprint.annotation.models.video as gfav
import global_finprint.annotation.models.animal as gfaa
import global_finprint.annotation.models.observation as gfao
import global_finprint.annotation.models.annotation as gfan
from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction

FRAME_FIELD_LENGTH = 32
CAMERA_FIELD_LENGTH = 32

LEGACY_USER_FORMAT = 'LEGACY_{}'
LEGACY_EMAIL_FORMAT = '{}@sink.arpa'
LEGACY_AFFILITATION = 'Legacy'
LEGACY_COMMENT = 'Auto-imported data.'

DEFAULT_ASSIGNMENT_STATUS = 'Ready for review'

UNDETERMINED_HABITAT_TYPE = 'To Be Updated'

logger = logging.getLogger('scripts')
animal_map = None

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

@functools.lru_cache()
def get_animal_sex_map():
    return make_choices_reverse_map(gfaa.ANIMAL_SEX_CHOICES)

@functools.lru_cache()
def get_animal_stage_map():
    return make_choices_reverse_map(gfaa.ANIMAL_STAGE_CHOICES)

def make_choices_reverse_map(choices_set):
    result = {}
    for abrev, verbose in choices_set:
        result[verbose.lower()] = abrev
        result[abrev.lower()] = abrev
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
            validate_data(location, 'No location found with name "{}"'.format(location_name))
            lead_candidates = djam.User.objects.filter(last_name=investigator)
            if len(lead_candidates) == 0:
                lead = get_user(investigator, 'investigator')
            else:
                validate_data(
                    len(lead_candidates) < 2,
                    'More than one investigator with last name {}'.format(investigator))
                lead = gfcm.FinprintUser.objects.filter(user=lead_candidates[0]).first()
            validate_data(lead, 'No FinprintUser associated with "{}"'.format(investigator))

            team=gfcm.Team.objects.filter(lead=lead).first()
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
        source_video_str,
        aws_video_str,
        comment
):
    try:
        logger.info('Working on set "%s"', set_code)
        trip = gftm.Trip.objects.filter(code=trip_code).first()
        validate_data(trip, 'references non-existent trip "{}"'.format(trip_code))
        the_set = gfbm.Set.objects.filter(code=set_code, trip=trip).first()
        if not the_set:
            validate_data(drop_time, 'No drop time supplied.')
            if haul_time:
                validate_data(drop_time < haul_time, 'Drop time must be before haul time.')
            reef_habitat = get_reef_habitat(site_name, reef_name, habitat_type)
            equipment = parse_equipment_string(equipment_str)
            bait = parse_bait_string(bait_str)
            video = gfav.Video(file=aws_video_str, source_folder=source_video_str, user=get_import_user())
            video.save()
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
                video=video,
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
                    validate_data(
                        False,
                        'Bad tide_state "{}" for set "{}" of trip "{}"'.format(tide_state, set_code, trip_code))
            if wind_direction:
                wind_direction = wind_direction.upper()
            if surface_chop:
                try:
                    surface_chop = get_surface_chop_map()[surface_chop.lower()]
                except KeyError:
                    validate_data(
                        False,
                        'Bad surface chop "{}" for set "{}" of trip "{}"'.format(surface_chop, set_code, trip_code))

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

def import_observation(
        trip_code,
        set_code,
        obsv_date,
        obsv_time,
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
        annotation_date,
        raw_import_json
):
    try:
        logger.info(
            'Trying to add observation data from "%s" for set "%s" on trip "%s"',
            annotator,
            set_code,
            trip_code
        )

        with transaction.atomic():
            the_trip = gftm.Trip.objects.filter(code=trip_code).first()
            validate_data(the_trip, 'Trip "{}" not found when trying to import observation.'.format(trip_code))

            the_set = gfbm.Set.objects.filter(code=set_code, trip=the_trip).first()
            validate_data(the_set, 'Set "{}" not found when trying to import observation.'.format(set_code))
            validate_data(the_set.video, 'No video associated with set "{}"'.format(set_code))

            annotator_user = get_annotator(annotator)
            assignment = get_assignment(annotator_user, the_set.video)

            if does_observation_exist(assignment, duration, obsv_time, raw_import_json):
                logger.warning(
                    'Not importing: identical observation already exists from "%s" for set "%s" on trip "%s"',
                    annotator,
                    set_code,
                    trip_code
                )
            else:
                observation = gfao.Observation(
                    assignment=assignment,
                    duration=duration,
                    comment=LEGACY_COMMENT,
                    user=get_import_user()
                )
                observation.save()

                if family or genus:
                    observation.type = 'A'
                    observation.save()
                    animal_id = get_animal_mapping(family, genus, species)
                    if animal_id:
                        animal = gfaa.Animal.objects.get(pk=animal_id)
                    elif family == None:
                        animal = gfaa.Animal.objects.filter(
                            genus=genus,
                            species=species).first()
                    else:
                        animal = gfaa.Animal.objects.filter(
                            family=family,
                            genus=genus,
                            species=species
                        ).first()
                    validate_data(animal, 'Unable to find animal {} - {} - {}'.format(family, genus, species))
                    animal_obsv_args = {
                        'observation': observation,
                        'animal': animal,
                        'user': get_import_user()
                    }
                    if sex:
                        try:
                            animal_obsv_args['sex'] = get_animal_sex_map()[sex.lower()]
                        except KeyError:
                            validate_data(False, 'Unknown animal sex "{}"'.format(sex))
                    if length:
                        animal_obsv_args['length'] = length
                    if stage:
                        animal_obsv_args['stage'] = get_animal_stage_map()[stage.lower()]
                    animal_obsv = gfao.AnimalObservation(**animal_obsv_args)
                    animal_obsv.save()

                attribute_ids = []
                if behavior:
                    att, _  = gfan.Attribute.objects.get_or_create(name=behavior)
                    attribute_ids = [att.id]

                event = gfao.Event.create(
                    observation=observation,
                    event_time=obsv_time,
                    note=comment,
                    attribute=attribute_ids,
                    user=get_import_user(),
                    raw_import_json=raw_import_json
                )
                event.save()
                logger.info(
                    'Successfully added observation data from "%s" for set "%s" on trip "%s"',
                    annotator,
                    set_code,
                    trip_code
                )
    except DataError:
        logger.error('Failed while adding observation for set "%s" of trip "%s"', set_code, trip_code)

def update_set_data(trip_code, set_code, visibility):
    try:
        logger.info('Updating set data for set "{}" of trip "{}"'.format(set_code, trip_code))
        the_trip = gftm.Trip.objects.filter(code=trip_code).first()
        validate_data(the_trip, 'Trip "{}" not found when trying to import observation.'.format(trip_code))

        the_set = gfbm.Set.objects.filter(code=set_code, trip=the_trip).first()
        validate_data(the_set, 'Set "{}" not found when trying to import observation.'.format(set_code))

        the_set.visibility = visibility
        the_set.save()
    except DataError:
        logger.error('Failed to update visibility for set "{}" of trip "{}"'.format(set_code, trip_code))

def load_animal_mapping(mapping_file):
    global animal_map
    animal_map = json.load(open(mapping_file))

def get_animal_mapping(family, genus, species):
    result = None
    try:
        if animal_map:
            result = animal_map[family][genus][species]
    except KeyError:
        pass # no special mapping for this animal
    return result

def does_observation_exist(
        assignment,
        duration,
        obsv_time,
        raw_import_json
):
    result = False
    event = gfao.Event.objects.filter(
        observation__assignment=assignment,
        observation__duration=duration,
        event_time=obsv_time,
        raw_import_json=raw_import_json
    ).first()
    if event:
        result = True
    return result

def get_assignment(annotator_user, video):
    assignment = gfav.Assignment.objects.filter(
        annotator=annotator_user,
        video=video
    ).first()
    if not assignment:
        assignment = gfav.Assignment(
            annotator=annotator_user,
            video=video,
            assigned_by=gfcm.FinprintUser.objects.filter(user=get_import_user()).first(),
            status=gfav.AnnotationState.objects.get(name=DEFAULT_ASSIGNMENT_STATUS),
            user=get_import_user()
        )
        assignment.save()
    return assignment

def get_user(full_name, column):
    validate_data(full_name, 'No {} specified.'.format(column))

    # check that we didn't just get a last name
    user_candidates = find_users_with_lastname(full_name)
    if user_candidates and len(user_candidates) == 1:
        return user_candidates.first()

    # deal with full names
    full_name = full_name.strip()
    anno_array = full_name.split(' ', maxsplit=1)
    validate_data(len(anno_array) == 2, 'Need both first and last name for {} "{}"'.format(column, full_name))
    first_name, last_name = anno_array
    django_user = djam.User.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).first()
    validate_data(django_user, 'No user found with first name "{}" and last name "{}"'.format(first_name, last_name))
    finprint_user = gfcm.FinprintUser.objects.filter(user=django_user).first()
    validate_data(finprint_user, 'No finprint user associated with django user for "{}"'.format(full_name))
    return finprint_user

def find_users_with_lastname(last_name):
    django_user = djam.User.objects.filter(last_name__iexact=last_name).first()
    if django_user:
        return gfcm.FinprintUser.objects.filter(user=django_user)
    else:
        return None

def get_annotator(annotator):
    return get_user(annotator, 'annotator')

def get_reef_habitat(site_name, reef_name, habitat_type):
    site = gfhm.Site.objects.filter(name__iexact=site_name).first()
    validate_data(site, 'Site "{}" not found'.format(site_name))

    reef = gfhm.Reef.objects.filter(name__iexact=reef_name, site=site).first()
    validate_data(reef, 'Reef "{}" not found'.format(reef_name))

    if not habitat_type:
        habitat_type = UNDETERMINED_HABITAT_TYPE
    reef_type = gfhm.ReefType.objects.filter(type__iexact=habitat_type).first()
    validate_data(reef_type, 'Unknown reef type: {}'.format(habitat_type))

    return gfhm.ReefHabitat.get_or_create(reef, reef_type)

def parse_equipment_string(equipment_str):
    if equipment_str == 'Stereo stainless rebar / GoPro3 Silver+':
        equipment = gfbm.Equipment.objects.get(pk=5)
        validate_data(equipment,'Equipment with id 5 missing.')
    else:
        equip_array = equipment_str.split('/')
        validate_data(
            len(equip_array) == 2,
            'Unexpected equipment string: "{}"'.format(equipment_str))
        frame_str = equip_array[0][:FRAME_FIELD_LENGTH].strip()
        camera_str = equip_array[1][:CAMERA_FIELD_LENGTH].strip()
        frame = gfbm.FrameType.objects.filter(type__iexact=frame_str).first()
        validate_data(frame, 'Unknown frame type "{}" in equipment string "{}"'.format(frame_str, equipment_str))
        equipment = gfbm.Equipment.objects.filter(
            camera=camera_str,
            frame_type=frame).first()
        validate_data(
            equipment,
            'No equipment model found with camera "{}" and frame "{}" (frame_str "{}")'.format(
                camera_str, frame_str, equipment_str))
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
            description__iexact=bait_description,
            type=bait_type).first()
        validate_data(bait, 'Unknown bait "{}"'.format(bait_str))
    return bait


def minutes2milliseconds(minutes):
    """
    Converts minutes to milliseconds.
    :param minutes: duration in minutes as string
    :return: duration in milliseconds as int
    """
    if minutes:
        return round(float(minutes) * 60 * 1000)
    else:
        return 0

def time2milliseconds(the_time):
    """
    Converts the time part of a datetime to milliseconds.
    """
    result = 0
    if the_time:
        result += the_time.hour
        result *= 60
        result += the_time.minute
        result *= 60
        result += the_time.second
        result *= 1000
    return 0

def validate_data(predicate, error_msg):
    if not predicate:
        logger.error(error_msg)
        raise DataError()
