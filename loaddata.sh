#!/usr/bin/env bash

# load base lookup data
python manage.py loaddata global_finprint/core/fixtures/core_groups
python manage.py loaddata global_finprint/core/fixtures/core_affiliations
python manage.py loaddata global_finprint/core/fixtures/core_users
python manage.py loaddata global_finprint/core/fixtures/core_teams
python manage.py loaddata global_finprint/habitat/fixtures/habitat_locations
python manage.py loaddata global_finprint/habitat/fixtures/habitat_reef_mpa_substrate
python manage.py loaddata global_finprint/habitat/fixtures/habitat_site
python manage.py loaddata global_finprint/habitat/fixtures/habitat_reef
python manage.py loaddata global_finprint/habitat/fixtures/habitat_reefhabitat
python manage.py loaddata global_finprint/annotation/fixtures/annotation_status
python manage.py loaddata global_finprint/annotation/fixtures/annotation_animal
python manage.py loaddata global_finprint/annotation/fixtures/annotation_attribute
python manage.py loaddata global_finprint/bruv/fixtures/bruv_equipment
python manage.py loaddata global_finprint/trip/fixtures/trip_source
python manage.py loaddata global_finprint/trip/fixtures/trip_trip

# load test data
python manage.py loaddata global_finprint/core/fixtures/test_users
python manage.py loaddata global_finprint/annotation/fixtures/test_animal
python manage.py loaddata global_finprint/bruv/fixtures/test_set
python manage.py loaddata global_finprint/annotation/fixtures/test_videos
python manage.py loaddata global_finprint/annotation/fixtures/test_assignment
python manage.py loaddata global_finprint/annotation/fixtures/test_obs
