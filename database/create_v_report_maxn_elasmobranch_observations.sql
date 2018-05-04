--Create view showing maxn values for all sharks and rays, per set, and only using master observations

CREATE OR REPLACE VIEW public.v_report_maxn_elasmobranch_observations AS
  --Step 1: Get Reef and Location level descriptive variables
  -- Indicate which sets have completed master annotations
 WITH set_overview AS (
  WITH so AS (
  SELECT
  habitat_region.name AS region_name,
  habitat_location.name AS location_name,
  habitat_site.name AS site_name,
  habitat_reef.name AS reef_name,
  habitat_reeftype.type AS reef_type,
  habitat_reef.id AS reef_id,
  trip_trip.code AS trip_code,
  extract(YEAR FROM trip_trip.start_date) :: TEXT AS trip_year,
  bruv_set.id AS set_id,
  bruv_set.code AS set_code,
  bruv_set.latitude AS set_lat,
  bruv_set.longitude AS set_long,
  bruv_set.visibility,
  bruv_set.depth,
  bruv_bait.description AS bait,
  bruv_set.current_flow_estimated,
  bruv_set.current_flow_instrumented,
  annotation_masterrecord.id AS master_set_id,
  CASE WHEN annotation_masterrecord.status_id = 2 --status=2 means annotation is complete
  THEN 1
  ELSE 0
  END AS has_complete_master
  FROM habitat_region
  FULL OUTER JOIN habitat_location ON habitat_region.id = habitat_location.region_id
  FULL OUTER JOIN habitat_site ON habitat_location.id = habitat_site.location_id
  FULL OUTER JOIN habitat_reef ON habitat_site.id = habitat_reef.site_id
  FULL OUTER JOIN habitat_reefhabitat ON habitat_reef.id = habitat_reefhabitat.reef_id
  FULL OUTER JOIN habitat_reeftype ON habitat_reefhabitat.habitat_id = habitat_reeftype.id
  FULL OUTER JOIN bruv_set ON habitat_reefhabitat.id = bruv_set.reef_habitat_id
  LEFT JOIN trip_trip ON bruv_set.trip_id = trip_trip.id
  LEFT JOIN annotation_masterrecord ON bruv_set.id = annotation_masterrecord.set_id
  LEFT JOIN bruv_bait ON bruv_set.bait_id = bruv_bait.id
  )
  SELECT *
  FROM so
  WHERE set_id IS NOT NULL ), --take out sets and reefs that don't have any data,

---------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------
--Step 2: Clean observation data to enable calculation of maxn

--2.1 make a table of all master animal observations
-- only use master annotations, and of those only complete records
-- fill in null or empty values as 1

master_obs AS (
  SELECT
    annotation_masterrecord.set_id,
    annotation_masterrecord.id      AS master_set,
    annotation_masterobservation.id AS masterobservation_id,
    annotation_masterobservation.type,
    annotation_masterevent.id       AS masterevent_id,
    annotation_masterevent.event_time,
    CASE WHEN annotation_mastereventmeasurable.value='' OR annotation_mastereventmeasurable.value IS NULL
      THEN '1'
        ELSE annotation_mastereventmeasurable.value
          END AS value,
    annotation_mastereventmeasurable.measurable_id,
    annotation_masteranimalobservation.animal_id
  FROM annotation_masterrecord
    LEFT JOIN annotation_masterobservation ON annotation_masterrecord.id = annotation_masterobservation.master_record_id
    FULL OUTER JOIN annotation_masterevent
      ON annotation_masterobservation.id = annotation_masterevent.master_observation_id
    LEFT JOIN annotation_mastereventmeasurable
      ON annotation_masterevent.id = annotation_mastereventmeasurable.master_event_id
    LEFT JOIN annotation_masteranimalobservation
      ON annotation_masterobservation.id = annotation_masteranimalobservation.master_observation_id
  WHERE annotation_masterobservation.id IS NOT NULL
        AND annotation_masterrecord.status_id = 2
        AND type='A'),

-------------------------------------------------------------------------------------------------------

-- Step 2.2 - deal with observations where multiple entries exist for the same measurable
-- search for all sets where multiple entries for same species at same time, where measurable>1
-- select greatest maxn value for each set/species/time combo

 duplicate_records AS (
SELECT
  set_id,
  master_set,
  event_time,
  animal_id,
  count(masterobservation_id)   AS num_records,
  max(value::INT)                 AS max_value,
  sum(value::INT)/count(masterobservation_id)         AS value_per_record
  FROm master_obs
    GROUP BY set_id, master_set, event_time, animal_id),

  dr2 AS (
  SELECT
  set_id,
  master_set,
  event_time,
  animal_id,
  max_value AS value
  FROM duplicate_records WHERE num_records>1 AND value_per_record>1),

  -- remove duplicate records from master_obs ...
  master_obs_keep AS (
SELECT
  m.set_id,
  m.master_set,
  m.event_time,
  m.animal_id,
  m."value"::INT
FROM master_obs m
LEFT JOIN dr2 ON m.set_id=dr2.set_id AND m.event_time=dr2.event_time AND m.animal_id=dr2.animal_id
WHERE dr2.value IS NULL),

-- and replace with corrected values
  master_obs2 AS (
SELECT * FROM master_obs_keep
UNION ALL
  SELECT * FROM dr2),

-----------------------------------------------------------------------------------------------------------------
-- Step 2.3 - aggregate values where >1 observation for same species/time/set
-- this is for the sets where all individuals were recorded separately without indicating a maxn value (e.g. Global Archive legacy data)

master_obs3 AS (
SELECT
  set_id,
  master_set,
  event_time,
  animal_id,
  sum(value)  AS "value"
FROM master_obs2
GROUP BY set_id, master_set, event_time, animal_id),


--------------------------------------------------------------------------------------------------------
-- STEP 3 - Calculate maxn
-- make a table of zero times
zero_times AS (
  SELECT
    master_attribute_summary.master_record_id,
    master_attribute_summary.video_id,
    max(
        CASE
        WHEN (master_attribute_summary.zero_time_tagged = 0)
          THEN 0
        ELSE master_attribute_summary.event_time
        END) AS zero_time
  FROM master_attribute_summary
  GROUP BY master_attribute_summary.master_record_id, master_attribute_summary.video_id),

 maxn AS (
  --  add zero time, and calculate adjusted time for each event
  WITH   em2 AS (
      SELECT
        master_obs3.set_id,
        master_obs3.master_set,
        master_obs3."value",
        master_obs3.animal_id,
        zero_times.zero_time,
        (master_obs3.event_time - zero_times.zero_time) AS event_time_adj
      FROM master_obs3
        LEFT JOIN zero_times
          ON master_obs3.master_set = zero_times.master_record_id),

    -- remove events with times over 1 hour, or less than 0
      em3 AS (
        SELECT
          em2.set_id,
          em2.master_set,
          em2."value",
          em2.animal_id,
          em2.event_time_adj,
          text_time(event_time_adj) AS event_time_adj_mins
        FROM em2
        WHERE em2.event_time_adj < 3600001 AND -- 3.6 million milliseconds in an hour
              em2.event_time_adj > 0),
    --select greatest maxn per animal per set
      max_maxn AS (
        SELECT
          max(value) AS maxn,
          animal_id,
          set_id,
          master_set
        FROM em3
        GROUP BY animal_id, set_id, master_set),

    -- select earliest observation per maxn per animal per set
      em5 AS (
        SELECT
          "value",
          animal_id,
          set_id,
          master_set,
          min(em3.event_time_adj)      AS min_event_time_milli,
          min(em3.event_time_adj_mins) AS min_event_time_mins
        FROM em3
        GROUP BY "value", animal_id, set_id, master_set)

  --link max maxn (em4) with times from em5
  SELECT
    max_maxn.maxn,
    max_maxn.animal_id,
    max_maxn.set_id,
    max_maxn.master_set,
    em5.min_event_time_mins,
    em5.min_event_time_milli
  FROM max_maxn
    LEFT JOIN em5 ON max_maxn.maxn = em5."value"
                     AND max_maxn.animal_id = em5.animal_id
                     AND max_maxn.set_id = em5.set_id
                    AND max_maxn.master_set=em5.master_set),

maxnsharks AS (
  SELECT
    maxn,
    animal_id,
    set_id,
    master_set,
    min_event_time_milli,
    min_event_time_mins
  FROM maxn
    LEFT JOIN annotation_animal ON maxn.animal_id = annotation_animal.id
  WHERE group_id IN (1, 2)
),
-----------------------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------------------------------------
--Step 3 - pull together lists of sets, species names, and maxn values
--use set overview as the base, then add maxn, then add species names
 animals AS (
  SELECT
    annotation_animal.id,
    annotation_animal.common_name,
    annotation_animal.genus,
    annotation_animal.species,
    annotation_animal.family,
    annotation_animalgroup.name AS species_group
  FROM annotation_animal
    LEFT JOIN annotation_animalgroup ON annotation_animal.group_id = annotation_animalgroup.id)

  --final output:
SELECT
  region_name,
  set_overview.location_name,
  site_name,
  reef_name,
  reef_type,
  trip_code,
  trip_year,
  set_overview.set_code,
  maxnsharks.maxn,
  common_name,
  genus,
  species,
  species_group,
  family,
  maxnsharks.min_event_time_milli AS event_time_mil,
  maxnsharks.min_event_time_mins  AS event_time_mins,
  set_lat,
  set_long,
  visibility,
  depth,
  bait,
  current_flow_estimated,
 current_flow_instrumented,
   set_overview.reef_id,
     set_overview.set_id,
  set_overview.master_set_id,
   CASE WHEN (maxnsharks.animal_id IS NULL)
    THEN 9999
  ELSE maxnsharks.animal_id
  END                       AS animal_id
FROM set_overview
  LEFT JOIN maxnsharks ON set_overview.set_id = maxnsharks.set_id AND set_overview.master_set_id=maxnsharks.master_set
  LEFT JOIN animals ON animals.id = maxnsharks.animal_id
WHERE has_complete_master=1;

-- FIN --

