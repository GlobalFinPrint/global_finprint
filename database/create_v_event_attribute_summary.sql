CREATE VIEW public.event_attribute_summary AS
  SELECT
    trip.code                                  AS trip_code,
    s.code                                     AS set_code,
    trip.id                                    AS trip_id,
    s.id                                       AS set_id,
    s.reef_habitat_id,
    vid.id                                     AS video_id,
    assig.id                                   AS assignment_id,
    assig.annotator_id,
    obs.id                                     AS observation_id,
    evt.id                                     AS event_id,
    animal.id                                  AS animal_id,
    evt.event_time,
    CASE
    WHEN (evt.note = 'Time on seabed' :: TEXT)
      THEN 1
    ELSE 0
    END                                        AS zero_time_em_note,
    CASE
    WHEN (evt.note = 'Time off seabed' :: TEXT)
      THEN 1
    ELSE 0
    END                                        AS haul_time_em_note,
    CASE
    WHEN (EXISTS(SELECT evtat.id
                 FROM annotation_event_attribute evtat
                 WHERE ((evtat.attribute_id = 16) AND (evtat.event_id = evt.id))))
      THEN 1
    ELSE 0
    END                                        AS zero_time_tagged,
    CASE
    WHEN (EXISTS(SELECT evtat.id
                 FROM annotation_event_attribute evtat
                 WHERE ((evtat.attribute_id = 33) AND (evtat.event_id = evt.id))))
      THEN 1
    ELSE 0
    END                                        AS sixty_minute_time_tagged,
    CASE
    WHEN (EXISTS(SELECT evtat.id
                 FROM annotation_event_attribute evtat
                 WHERE ((evtat.attribute_id = 24) AND (evtat.event_id = evt.id))))
      THEN 1
    ELSE 0
    END                                        AS ninty_minute_time_tagged,
    CASE
    WHEN (EXISTS(SELECT evtat.id
                 FROM annotation_event_attribute evtat
                 WHERE ((evtat.attribute_id = 23) AND (evtat.event_id = evt.id))))
      THEN 1
    ELSE 0
    END                                        AS haul_time_tagged,
    CASE
    WHEN (EXISTS(SELECT evtat.id
                 FROM annotation_event_attribute evtat
                 WHERE ((evtat.attribute_id = 13) AND (evtat.event_id = evt.id))))
      THEN 1
    ELSE 0
    END                                        AS max_n_tagged,
    "substring"(evt.note, '[0-9]+' :: TEXT)    AS numeric_value_from_event_note,
    "substring"(obs.comment, '[0-9]+' :: TEXT) AS numeric_value_from_obs_comment
  FROM (((((((trip_trip trip
    JOIN bruv_set s ON ((s.trip_id = trip.id)))
    JOIN annotation_video vid ON ((vid.id = s.video_id)))
    JOIN annotation_assignment assig ON ((assig.video_id = vid.id)))
    JOIN annotation_observation obs ON ((obs.assignment_id = assig.id)))
    JOIN annotation_event evt ON ((evt.observation_id = obs.id)))
    LEFT JOIN annotation_animalobservation anobs ON ((anobs.observation_id = obs.id)))
    LEFT JOIN annotation_animal animal ON ((animal.id = anobs.animal_id)));
