CREATE OR REPLACE VIEW public.v_report_observations_coral_summary AS
WITH zero_times as
(
  select
    set_id,
    video_id,
    max(
        case
          when zero_time_tagged = 0
          then 0
          else event_time
        end) as zero_time
  from event_attribute_summary
  group by set_id,
    video_id
)
SELECT
  evtsum.trip_code,
  evtsum.set_code,
  evtsum.trip_code || '_' || evtsum.set_code                   AS full_code,

  hab.region                                                   AS region,
  hab.location                                                 AS location,
  hab.site                                                     AS site,
  hab.reef                                                     AS reef,
  hab.reef_habitat                                             AS reef_habitat,

  ani.family,
  ani.genus,
  ani.species,

  min(evtsum.event_time_minutes)                               AS event_time_minutes_raw,
  min(public.text_time(evtsum.event_time - z.zero_time))       AS event_time_minutes,
  max(evtsum.numeric_value_from_event_note)                    AS maxn,

  evtsum.trip_id,
  evtsum.set_id,
  evtsum.video_id
FROM
  event_attribute_summary evtsum
  inner join zero_times z on z.video_id = evtsum.video_id
  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = evtsum.reef_habitat_id

  INNER JOIN core_finprintuser fu ON fu.id = evtsum.annotator_id
  INNER JOIN auth_user u ON u.id = fu.user_id

  INNER JOIN annotation_animalobservation aobs ON aobs.observation_id = evtsum.observation_id
  INNER JOIN annotation_animal ani ON ani.id = aobs.animal_id
WHERE hab.region = 'Coral Triangle'
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
  family,
  genus,
  species,
  evtsum.trip_id,
  evtsum.set_id,
  evtsum.video_id
ORDER BY
  full_code,
  event_time_minutes_raw;


