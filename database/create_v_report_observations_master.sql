CREATE OR REPLACE VIEW public.v_report_observations_master AS
  SELECT
  tr.code                                                   AS trip_code,
  s.code                                                    AS set_code,
  tr.code || '_' || s.code                                  AS full_code,

    hab.region_name                                                   AS region_name,
  hab.location_name                                                 AS location_name,
  hab.site_name                                                     AS site_name,
  hab.reef_name                                                     AS reef_name,
  hab.reef_habitat_name                                             AS reef_habitat_name,

  mas.event_time,
  mas.event_time_minutes,

  mas.observation_comment,
  mas.event_note,
  mas.observation_type,

  meas.value                                                        AS measurable,

  ani.family,
  ani.genus,
  ani.species,

  mas.zero_time_tagged,
  mas.sixty_minute_time_tagged,
  mas.ninty_minute_time_tagged                          AS ninety_minute_time_tagged,
  mas.haul_time_tagged,

  mas.max_n_tagged,
  mas.numeric_value_from_event_note,

  tr.id                                                     AS trip_id,
  s.id                                                      AS set_id,
  hab.region_id,
  hab.location_id,
  hab.site_id,
  hab.reef_id,
  hab.reef_habitat_id,
  mas.master_record_id,
  mas.master_record_state_id,
  mas.master_record_state
FROM
  trip_trip tr
  INNER JOIN bruv_set s ON s.trip_id = tr.id

  INNER JOIN habitat_summary hab on hab.reef_habitat_id = s.reef_habitat_id

  INNER JOIN master_attribute_summary mas on mas.set_id = s.id

  LEFT JOIN annotation_mastereventmeasurable meas on mas.event_id=meas.master_event_id

  LEFT JOIN annotation_animal ani ON ani.id = mas.animal_id
ORDER BY
  full_code,
  event_time;


