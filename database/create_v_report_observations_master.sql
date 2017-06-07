CREATE OR REPLACE VIEW public.v_report_observations_master AS
  SELECT
  tr.code                                                   AS trip_code,
  s.code                                                    AS set_code,
  tr.code || '_' || s.code                                  AS full_code,

  hrg.name                                                  AS region,
  hlc.name                                                  AS location,
  hst.name                                                  AS site,
  hrf.name                                                  AS reef,
  hrt.description                                           AS reef_habitat,

  evt.event_time,
  -- format event time to xx:xx:xxx
  lpad((((evt.event_time / 1000) / 60) :: TEXT), 3, '0')
  || ':' || lpad(((evt.event_time / 1000) % 60) :: TEXT, 2, '0')
  || ':' || lpad(((evt.event_time % 1000) :: TEXT), 3, '0') AS event_time_minutes,

  obs.comment,
  evt.note,

  ani.family,
  ani.genus,
  ani.species,

  CASE
  WHEN evt.note = 'Time on seabed'
    THEN 1
  WHEN exists(
      SELECT evtat.id
      FROM annotation_event_attribute evtat
        INNER JOIN annotation_attribute at ON at.id = evtat.attribute_id
      WHERE evtat.event_id = evt.id
            AND lower(at.name) = 'mark zero time'
  )
    THEN 1
  ELSE 0
  END                                                       AS zero_time,
  CASE
  WHEN evt.note = 'Time off seabed'
    THEN 1
  WHEN exists(
      SELECT evtat.id
      FROM annotation_event_attribute evtat
        INNER JOIN annotation_attribute at ON at.id = evtat.attribute_id
      WHERE evtat.event_id = evt.id
            AND lower(at.name) = 'mark haul time'
  )
    THEN 1
  ELSE 0
  END                                                       AS haul_time,

  CASE
  WHEN exists(
      SELECT evtat.id
      FROM annotation_event_attribute evtat
        INNER JOIN annotation_attribute at ON at.id = evtat.attribute_id
      WHERE evtat.event_id = evt.id
            AND lower(at.name) = 'maxn image frame'
  )
    THEN 1
  ELSE 0
  END                                                       AS max_n_update,
  CASE
  WHEN exists(
      SELECT evtat.id
      FROM annotation_event_attribute evtat
        INNER JOIN annotation_attribute at ON at.id = evtat.attribute_id
      WHERE evtat.event_id = evt.id
            AND lower(at.name) = 'maxn image frame'
  )
    THEN substring(obs.comment FROM '[0-9]+')
  ELSE NULL
  END                                                       AS max_n_from_comment,

  tr.id                                                     AS trip_id,
  s.id                                                      AS set_id,
  mas.id                                                    AS master_record_id,
  ms.id                                                     AS master_record_state_id,
  ms.name                                                   AS master_record_state
FROM
  trip_trip tr
  INNER JOIN bruv_set s ON s.trip_id = tr.id

  INNER JOIN habitat_reefhabitat hrh ON hrh.id = s.reef_habitat_id
  INNER JOIN habitat_reef hrf ON hrf.id = hrh.reef_id
  INNER JOIN habitat_site hst ON hst.id = hrf.site_id
  INNER JOIN habitat_location hlc ON hlc.id = hst.location_id
  INNER JOIN habitat_region hrg ON hrg.id = hlc.region_id
  INNER JOIN habitat_reeftype hrt ON hrt.id = hrh.habitat_id

  INNER JOIN annotation_masterrecord mas ON mas.set_id = s.id
  INNER JOIN annotation_masterrecordstate ms ON ms.id = mas.status_id

  INNER JOIN annotation_masterobservation obs ON obs.master_record_id = mas.id
  INNER JOIN annotation_masterevent evt ON evt.master_observation_id = obs.id

  LEFT JOIN annotation_masteranimalobservation aobs ON aobs.master_observation_id = obs.id
  LEFT JOIN annotation_animal ani ON ani.id = aobs.animal_id

ORDER BY
  full_code,
  event_time;


