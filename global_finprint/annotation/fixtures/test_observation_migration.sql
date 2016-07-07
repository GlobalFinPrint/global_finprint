-- test data for observation data migration testing.

--- delete from annotation_animalobservation;
--- delete from annotation_observation;


INSERT INTO annotation_observation (
  id,
  create_datetime,
  last_modified_datetime,
  initial_observation_time,
  type,
  duration,
  assignment_id,
  user_id,
  extent,
  comment
)
VALUES
  (
    1,
    '2015-11-03T19:00:22.080Z' :: TIMESTAMP,
    '2015-11-03T19:03:16.655Z' :: TIMESTAMP,
    12345,
    'A',
    15,
    1,
    1,
    ST_GeomFromEWKT('SRID=4326;POLYGON((75.15 29.53,77 29,77.6 29.5,75.15 29.53))'),
    ''
  ),
  (
    2,
    '2015-11-03T19:00:22.080Z' :: TIMESTAMP,
    '2015-11-03T19:03:16.655Z' :: TIMESTAMP,
    22000,
    'A',
    22,
    1,
    1,
    NULL,
    'tasty fish'
  ),
  (3,
   '2015-11-03T19:00:22.080Z' :: TIMESTAMP,
   '2015-11-03T19:03:16.655Z' :: TIMESTAMP,
   12345,
   'I',
   200,
   1,
   1,
   ST_GeomFromEWKT('SRID=4326;POLYGON ((30 10, 10 20, 20 40, 40 40, 30 10))'),
   'something interesting!'
  );

INSERT INTO annotation_animalobservation
(id, create_datetime, last_modified_datetime, sex, stage, user_id, observation_id, animal_id)
VALUES
  (
    1,
    '2015-11-03T19:00:22.080Z',
    '2015-11-03T19:03:16.655Z',
    'U',
    'U',
    1,
    1,
    16
  ),
  (
    2,
    '2015-11-03T19:00:22.080Z',
    '2015-11-03T19:03:16.655Z',
    'U',
    'U',
    1,
    2,
    46
  );
