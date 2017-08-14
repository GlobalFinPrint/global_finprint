BEGIN TRANSACTION;

-- annotators
INSERT INTO annotation_eventmeasurable
(
  event_id,
  value,
  measurable_id
)
  SELECT DISTINCT
    evt.id                                  AS event_id,
    "substring"(evt.note, '[0-9]+' :: TEXT) AS numeric_value_from_event_note,
    2                                       AS measurable_id
  FROM (((((((trip_trip trip
    INNER JOIN bruv_set s ON ((s.trip_id = trip.id)))
    INNER JOIN annotation_video vid ON ((vid.id = s.video_id)))
    INNER JOIN annotation_assignment assig ON ((assig.video_id = vid.id)))
    INNER JOIN annotation_observation obs ON ((obs.assignment_id = assig.id)))
    INNER JOIN annotation_event evt ON ((evt.observation_id = obs.id)))
    INNER JOIN annotation_animalobservation anobs ON ((anobs.observation_id = obs.id)))
    INNER JOIN annotation_animal animal ON ((animal.id = anobs.animal_id)))
  WHERE CASE
        WHEN (EXISTS(SELECT evtat.id
                     FROM annotation_event_attribute evtat
                     WHERE ((evtat.attribute_id = 13) AND (evtat.event_id = evt.id))))
          THEN 1
        ELSE 0
        END = 1
        AND "substring"(evt.note, '[0-9]+' :: TEXT) IS NOT NULL
        AND evt.id NOT IN (SELECT event_id
                           FROM annotation_eventmeasurable);

-- master
INSERT INTO annotation_mastereventmeasurable
(
  value,
  master_event_id,
  measurable_id
)
  SELECT DISTINCT
    "substring"(evt.note, '[0-9]+' :: TEXT) AS value,
    evt.id,
    2                                       AS measurable_id
  FROM trip_trip trip
    INNER JOIN bruv_set s ON (s.trip_id = trip.id)
    INNER JOIN annotation_masterrecord mas ON mas.set_id = s.id
    INNER JOIN annotation_masterobservation obs ON obs.master_record_id = mas.id
    INNER JOIN annotation_masterevent evt ON evt.master_observation_id = obs.id
    LEFT JOIN annotation_masterevent_attribute att ON att.masterevent_id = evt.id
  WHERE att.attribute_id = 13
        AND "substring"(evt.note, '[0-9]+' :: TEXT) IS NOT NULL
        AND evt.id NOT IN (SELECT master_event_id
                           FROM annotation_mastereventmeasurable);

COMMIT TRANSACTION;
