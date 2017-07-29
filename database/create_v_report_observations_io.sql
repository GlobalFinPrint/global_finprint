CREATE OR REPLACE VIEW public.v_report_observations_io AS
SELECT
  tr.code                                                   AS trip_code,
  s.code                                                    AS set_code,
  tr.code || '_' || s.code                                  AS full_code,

  hab.region_name                                                   AS region_name,
  hab.location_name                                                 AS location_name,
  hab.site_name                                                     AS site_name,
  hab.reef_name                                                     AS reef_name,
  hab.reef_habitat_name                                             AS reef_habitat_name,

  u.first_name || ' ' || u.last_name                        AS annotator,

  evt.event_time,
  evt.event_time_minutes,

  evt.observation_comment,
  evt.event_note,

  ani.family,
  ani.genus,
  ani.species,

  evt.zero_time_tagged,
  evt.sixty_minute_time_tagged,
  evt.ninty_minute_time_tagged,
  evt.haul_time_tagged,

  evt.max_n_tagged,
  evt.numeric_value_from_event_note,


  tr.id                                                     AS trip_id,
  s.id                                                      AS set_id,
  hab.region_id,
  hab.location_id,
  hab.site_id,
  hab.reef_id,
  hab.reef_habitat_id,
  v.id                                                      AS video_id,
  a.id                                                      AS assignment_id,
  ast.id                                                    AS assignment_state_id,
  ast.name                                                  AS assignment_state
FROM
  trip_trip tr
  INNER JOIN bruv_set s ON s.trip_id = tr.id

  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = s.reef_habitat_id

  INNER JOIN annotation_video v ON v.id = s.video_id
  INNER JOIN annotation_assignment a ON a.video_id = v.id
  INNER JOIN annotation_annotationstate ast ON ast.id = a.status_id

  INNER JOIN event_attribute_summary evt on evt.assignment_id = a.id

  INNER JOIN core_finprintuser fu ON fu.id = evt.annotator_id
  INNER JOIN auth_user u ON u.id = fu.user_id

  LEFT JOIN annotation_animal ani ON ani.id = evt.animal_id
WHERE hab.region_name = 'Indian Ocean'
ORDER BY
  full_code,
  event_time,
  annotator;
