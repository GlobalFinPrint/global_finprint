CREATE OR REPLACE VIEW public.v_report_observations_wa_summary AS
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
),
    -- maxn by event count by set
    event_count_maxn AS
(
    SELECT
      count(evt.id) AS event_count,
      evt.event_time,
      aobs.animal_id,

      s.id as set_id,
      evt.observation_id
    FROM annotation_event evt
      INNER JOIN annotation_animalobservation aobs ON aobs.observation_id = evt.observation_id
      INNER JOIN annotation_observation obs ON obs.id = evt.observation_id
      INNER JOIN annotation_assignment assig ON assig.id = obs.assignment_id
      INNER JOIN bruv_set s ON s.video_id = assig.video_id
    GROUP BY
      evt.event_time,
      evt.observation_id,
      aobs.animal_id,
      s.id
),
    -- maxn from attribute and note by set
    attribute_maxn AS
(
    SELECT
      max(evtsum.numeric_value_from_event_note) :: BIGINT    AS note_count,
      evtsum.event_time,
      aobs.animal_id,

      evtsum.set_id
    FROM event_attribute_summary evtsum
        INNER JOIN annotation_animalobservation aobs ON aobs.observation_id = evtsum.observation_id
    WHERE evtsum.numeric_value_from_event_note IS NOT NULL
          AND evtsum.max_n_tagged = 1
    GROUP BY
      evtsum.event_time,
      aobs.animal_id,
      evtsum.set_id
),
    -- merged results
    full_maxn as
(
  SELECT
    case when not(event_count is null) and not(note_count is null)
    then
      case
        when event_count > note_count
        then event_count
        else note_count
      end
    else coalesce(ecm.event_count, atm.note_count)
    end AS maxn,
    coalesce(ecm.event_time, atm.event_time) as event_time,
    coalesce(ecm.animal_id, atm.animal_id) as animal_id,
    coalesce(ecm.set_id, atm.set_id) as set_id
  FROM event_count_maxn ecm
  FULL OUTER JOIN attribute_maxn atm ON (
      ecm.event_time = atm.event_time
      and ecm.animal_id = atm.animal_id
      and ecm.set_id = atm.set_id
    )
),
  -- reduced to only "max" maxn as some record increases
  reduced_maxn as
(
  SELECT
    max(maxn) as maxn,
    animal_id,
    set_id
  FROM full_maxn
  GROUP BY animal_id,
    set_id
)
-- earliest occurance of maxn + a bunch of other useful data
SELECT
  t.code as trip_code,
  s.code as set_code,
  t.code || '_' || s.code                        AS full_code,

  hab.region_name                                 AS region_name,
  hab.location_name                               AS location_name,
  hab.site_name                                   AS site_name,
  hab.reef_name                                   AS reef_name,
  hab.reef_habitat_name                           AS reef_habitat_name,

  ani.id as animal_id,
  ani.family,
  ani.genus,
  ani.species,

  reduced_maxn.maxn,
  public.text_time(min(full_maxn.event_time))               AS event_time_minutes_raw,
  public.text_time(min(full_maxn.event_time) - min(z.zero_time)) AS event_time_minutes,

  t.id as trip_id,
  s.id                                            AS set_id,
  s.video_id

FROM reduced_maxn
  inner join full_maxn on (
    full_maxn.maxn = reduced_maxn.maxn
    and full_maxn.animal_id = reduced_maxn.animal_id
    and full_maxn.set_id = reduced_maxn.set_id
    )
  INNER JOIN annotation_animal ani ON ani.id = reduced_maxn.animal_id
  INNER JOIN bruv_set s ON s.id = reduced_maxn.set_id
  INNER JOIN trip_trip t ON t.id = s.trip_id

  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = s.reef_habitat_id
  INNER JOIN zero_times z ON z.video_id = s.video_id
where
  hab.region_name = 'Western Atlantic'
group by
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
