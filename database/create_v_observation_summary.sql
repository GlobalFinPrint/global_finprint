CREATE OR REPLACE VIEW public.observation_summary AS
WITH
    zero_times AS (
      SELECT
        event_attribute_summary.set_id,
        event_attribute_summary.video_id,
        max(
            CASE
            WHEN (event_attribute_summary.zero_time_tagged = 0)
              THEN 0
            ELSE event_attribute_summary.event_time
            END) AS zero_time
      FROM event_attribute_summary
      GROUP BY event_attribute_summary.set_id, event_attribute_summary.video_id
  ),
    event_measurable AS (
      SELECT
        evt_meas.value AS maxn,
        evt.event_time,
        aobs.animal_id,
        s.id           AS set_id,
        evt.observation_id
      FROM ((((
          annotation_measurable meas
          INNER JOIN annotation_eventmeasurable evt_meas ON evt_meas.measurable_id = meas.id
          INNER JOIN annotation_event evt ON evt.id = evt_meas.event_id
          JOIN annotation_animalobservation aobs ON ((aobs.observation_id = evt.observation_id)))
        JOIN annotation_observation obs ON ((obs.id = evt.observation_id)))
        JOIN annotation_assignment assig ON ((assig.id = obs.assignment_id)))
        JOIN bruv_set s ON ((s.video_id = assig.video_id)))
      WHERE meas.name = 'MaxN'
  ),
    reduced_maxn AS (
      SELECT
        max(em.maxn) AS maxn,
        em.animal_id,
        em.set_id
      FROM event_measurable em
      GROUP BY em.animal_id, em.set_id
  )
-- earliest occurance of maxn + a bunch of other useful data
SELECT
  row_number()
  OVER ()                                                               AS summary_id,
  t.code                                                                AS trip_code,
  s.code                                                                AS set_code,
  t.code || '_' || s.code                                               AS full_code,

  hab.region_name                                                       AS region_name,
  hab.location_name                                                     AS location_name,
  hab.site_name                                                         AS site_name,
  hab.reef_name                                                         AS reef_name,
  hab.reef_habitat_name                                                 AS reef_habitat_name,

  ani.id                                                                AS animal_id,
  ani.family,
  ani.genus,
  ani.species,

  reduced_maxn.maxn,
  public.text_time(min(event_measurable.event_time))                    AS event_time_minutes_raw,
  public.text_time(min(event_measurable.event_time) - min(z.zero_time)) AS event_time_minutes,

  t.id                                                                  AS trip_id,
  s.id                                                                  AS set_id,
  s.video_id
FROM reduced_maxn
  INNER JOIN event_measurable ON (
    event_measurable.maxn = reduced_maxn.maxn
    AND event_measurable.animal_id = reduced_maxn.animal_id
    AND event_measurable.set_id = reduced_maxn.set_id
    )
  INNER JOIN annotation_animal ani ON ani.id = reduced_maxn.animal_id
  INNER JOIN bruv_set s ON s.id = reduced_maxn.set_id
  INNER JOIN trip_trip t ON t.id = s.trip_id

  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = s.reef_habitat_id
  INNER JOIN zero_times z ON z.video_id = s.video_id
GROUP BY
  t.code,
  s.code,
  full_code,

  reduced_maxn.maxn,
  hab.region_name,
  hab.location_name,
  hab.site_name,
  hab.reef_name,
  hab.reef_habitat_name,

  ani.id,
  ani.family,
  ani.genus,
  ani.species,
  t.id,
  s.id,
  s.video_id;
