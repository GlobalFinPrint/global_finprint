CREATE OR REPLACE VIEW public.master_attribute_summary AS
SELECT trip.code AS trip_code,
    s.code AS set_code,
    trip.id AS trip_id,
    s.id AS set_id,
    s.reef_habitat_id,
    mas.id AS video_id,
    mst.id AS master_status_id,
    mst.name AS master_status,
    obs.id AS observation_id,
    obs.type   AS observation_type,
    evt.id AS event_id,
    aobs.animal_id,
    evt.event_time,
    ((((lpad((((evt.event_time / 1000) / 60))::text, 3, '0'::text) || ':'::text) || lpad((((evt.event_time / 1000) % 60))::text, 2, '0'::text)) || ':'::text) || lpad(((evt.event_time % 1000))::text, 3, '0'::text)) AS event_time_minutes,
        CASE
            WHEN (evt.note = 'Time on seabed'::text) THEN 1
            ELSE 0
        END AS zero_time_em_note,
        CASE
            WHEN (evt.note = 'Time off seabed'::text) THEN 1
            ELSE 0
        END AS haul_time_em_note,
        CASE
            WHEN (EXISTS ( SELECT evtat.id
               FROM annotation_masterevent_attribute evtat
              WHERE ((evtat.attribute_id = 16) AND (evtat.masterevent_id = evt.id)))) THEN 1
            ELSE 0
        END AS zero_time_tagged,
        CASE
            WHEN (EXISTS ( SELECT evtat.id
               FROM annotation_masterevent_attribute evtat
              WHERE ((evtat.attribute_id = 33) AND (evtat.masterevent_id = evt.id)))) THEN 1
            ELSE 0
        END AS sixty_minute_time_tagged,
        CASE
            WHEN (EXISTS ( SELECT evtat.id
               FROM annotation_masterevent_attribute evtat
              WHERE ((evtat.attribute_id = 24) AND (evtat.masterevent_id = evt.id)))) THEN 1
            ELSE 0
        END AS ninty_minute_time_tagged,
        CASE
            WHEN (EXISTS ( SELECT evtat.id
               FROM annotation_masterevent_attribute evtat
              WHERE ((evtat.attribute_id = 23) AND (evtat.masterevent_id = evt.id)))) THEN 1
            ELSE 0
        END AS haul_time_tagged,
        CASE
            WHEN (EXISTS ( SELECT evtat.id
               FROM annotation_masterevent_attribute evtat
              WHERE ((evtat.attribute_id = 13) AND (evtat.masterevent_id = evt.id)))) THEN 1
            ELSE 0
        END AS max_n_tagged,
    "substring"(evt.note, '[0-9]+'::text) AS numeric_value_from_event_note,
    "substring"(obs.comment, '[0-9]+'::text) AS numeric_value_from_obs_comment,
    evt.note AS event_note,
    obs.comment AS observation_comment,
    mas.id AS master_record_id,
    mst.id AS master_record_state_id,
    mst.name AS master_record_state
   FROM ((((((trip_trip trip
     JOIN bruv_set s ON ((s.trip_id = trip.id)))
     JOIN annotation_masterrecord mas ON ((mas.set_id = s.id)))
     JOIN annotation_masterrecordstate mst ON ((mst.id = mas.status_id)))
     JOIN annotation_masterobservation obs ON ((obs.master_record_id = mas.id)))
     JOIN annotation_masterevent evt ON ((evt.master_observation_id = obs.id)))
     LEFT JOIN annotation_masteranimalobservation aobs ON ((aobs.master_observation_id = obs.id)));
