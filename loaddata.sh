#!/usr/bin/env bash

# create admin
python manage.py createsuperuser

# load base lookup data
python manage.py loaddata global_finprint/habitat/fixtures/habitat_locations
python manage.py loaddata global_finprint/annotation/fixtures/annotation_animal
python manage.py loaddata global_finprint/bruv/fixtures/bruv_equipment
python manage.py loaddata global_finprint/habitat/fixtures/habitat_reef_mpa_substrate
python manage.py loaddata global_finprint/annotation/fixtures/annotation_fp_leads

# load test data
python manage.py loaddata global_finprint/annotation/fixtures/test_annotator
python manage.py loaddata global_finprint/habitat/fixtures/test_site
python manage.py loaddata global_finprint/trip/fixtures/test_trip
python manage.py loaddata global_finprint/bruv/fixtures/test_set
python manage.py loaddata global_finprint/annotation/fixtures/test_obs
