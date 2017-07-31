CREATE OR REPLACE VIEW public.observation_summary AS
WITH zero_times AS
(
    SELECT
      set_id,
      video_id,
      max(
          CASE
          WHEN zero_time_tagged = 0
            THEN 0
          ELSE event_time
          END) AS zero_time
    FROM event_attribute_summary
    GROUP BY set_id,
      video_id
)
SELECT
  row_number() over () as summary_id,
  evtsum.trip_code,
  evtsum.set_code,
  evtsum.trip_code || '_' || evtsum.set_code             AS full_code,

  hab.region_name                                        AS region_name,
  hab.location_name                                      AS location_name,
  hab.site_name                                          AS site_name,
  hab.reef_name                                          AS reef_name,
  hab.reef_habitat_name                                  AS reef_habitat_name,

  ani.family,
  ani.genus,
  ani.species,

  min(evtsum.event_time_minutes)                         AS event_time_minutes_raw,
  min(public.text_time(evtsum.event_time - z.zero_time)) AS event_time_minutes,
  max(evtsum.numeric_value_from_event_note)              AS maxn,

  evtsum.trip_id,
  evtsum.set_id,
  evtsum.video_id
FROM
  event_attribute_summary evtsum
  INNER JOIN zero_times z ON z.video_id = evtsum.video_id
  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = evtsum.reef_habitat_id

  INNER JOIN core_finprintuser fu ON fu.id = evtsum.annotator_id
  INNER JOIN auth_user u ON u.id = fu.user_id

  INNER JOIN annotation_animalobservation aobs ON aobs.observation_id = evtsum.observation_id
  INNER JOIN annotation_animal ani ON ani.id = aobs.animal_id

WHERE
  evtsum.numeric_value_from_event_note IS NOT NULL
  AND evtsum.max_n_tagged = 1
GROUP BY
  trip_code,
  set_code,
  full_code,
  region_name,
  location_name,
  site_name,
  reef_name,
  reef_habitat_name,
  family,
  genus,
  species,
  evtsum.trip_id,
  evtsum.set_id,
  evtsum.video_id
ORDER BY
  full_code,
  event_time_minutes_raw;


