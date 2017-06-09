CREATE OR REPLACE VIEW public.v_report_observations_pac_summary AS
SELECT
  evtsum.trip_code,
  evtsum.set_code,
  evtsum.trip_code || '_' || evtsum.set_code                   AS full_code,

  hab.region                                                   AS region,
  hab.location                                                 AS location,
  hab.site                                                     AS site,
  hab.reef                                                     AS reef,
  hab.reef_habitat                                             AS reef_habitat,

  u.first_name || ' ' || u.last_name                           AS annotator,

  ani.family,
  ani.genus,
  ani.species,

  max(evtsum.numeric_value_from_event_note)                    AS maxn,

  evtsum.trip_id,
  evtsum.set_id,
  evtsum.video_id,
  evtsum.assignment_id,
  evtsum.assignment_status_id,
  ast.name                                                                             AS assignment_state,
  'https://data.globalfinprint.org/assignment/review/' || evtsum.assignment_id :: TEXT AS assignment_review_url
FROM
  event_attribute_summary evtsum

  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = evtsum.reef_habitat_id

  INNER JOIN core_finprintuser fu ON fu.id = evtsum.annotator_id
  INNER JOIN auth_user u ON u.id = fu.user_id

  INNER JOIN annotation_annotationstate ast ON ast.id = evtsum.assignment_status_id

  INNER JOIN annotation_animalobservation aobs ON aobs.observation_id = evtsum.observation_id
  INNER JOIN annotation_animal ani ON ani.id = aobs.animal_id
WHERE hab.region = 'Pacific'
    and evtsum.numeric_value_from_event_note is not null
    and evtsum.max_n_tagged = 1
GROUP BY
  trip_code,
  set_code,
  full_code,
  region,
  location,
  site,
  reef,
  reef_habitat,
  annotator,
  family,
  genus,
  species,
  evtsum.trip_id,
  evtsum.set_id,
  evtsum.video_id,
  evtsum.assignment_id,
  evtsum.assignment_status_id,
  ast.name
ORDER BY
  full_code,
  annotator;
