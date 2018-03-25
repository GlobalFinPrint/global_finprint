--Create view showing maxn values for all sharks and rays, per set, and only using master observations

CREATE OR REPLACE VIEW public.v_report_maxn_observations AS
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
  WHERE set_id IS NOT NULL ), --take out sets and reefs that don't have any data


---------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------
--Step 2: Get MaxN per species per set
-- first make a table of zero times
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
  GROUP BY event_attribute_summary.set_id, event_attribute_summary.video_id),

--make a table of all master animal observations
-- only use master annotations, and of those only complete records

master_obs AS (
  SELECT
    annotation_masterrecord.set_id,
    annotation_masterrecord.id      AS master_set,
    annotation_masterobservation.id AS masterobservation_id,
    annotation_masterobservation.type,
    annotation_masterevent.id       AS masterevent_id,
    annotation_masterevent.event_time,
    annotation_mastereventmeasurable.value,
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
        AND type = 'A'),


--Make another table including all observations tagged as being MaxN, and where maxn values are filled in
-- only use master annotations, and of those only complete records
 complete_obs AS (
  SELECT *
  FROM master_obs
  WHERE measurable_id = 2 AND
        value NOT LIKE ''
),

----------------------------------------------------------------------------------------------------------
-- Create secondary table for sets where no values given for maxn
-- assume that we don't need to calculate maxn values for sets where at least 1 measurable id was recorded and maxn values given
-- when a value is given, there is always a measurable id

-- step 1 - separate out all sets from master_obs that are not in the complete_obs list
 master_obs_nomaxn AS (
  WITH complete_sets AS (
  SELECT DISTINCT set_id FROM complete_obs
),
  no_meas_sets AS (
    SELECT DISTINCT set_id FROM master_obs
    WHERE value IS NULL OR value=''
  ),
    set_select AS (
  SELECT set_id FROM no_meas_sets WHERE
    set_id NOT IN (SELECT set_id FROM complete_sets))

-- step 2 - take sets where values not recorded and reconnect observations
  SELECT *
  FROM master_obs
  WHERE set_id IN (SELECT set_id
                   FROM set_select)
),

-- step 3 - aggregate maxn per set per animal per time for those sets where maxn values missing
 no_meas_maxn AS (
  SELECT
    count(masterobservation_id) AS "value",
    --count number of rows per set per time per species
    set_id,
    master_set,
    event_time,
    animal_id
  FROM master_obs_nomaxn
  GROUP BY set_id, master_set, event_time, animal_id),

-- NOTE you don't have to remove duplicate set ids from event_measurable, as that table has already filtered for sets with maxn measurables

  -- step 4 - restructure maxn values with no measurables so they match structure of complete_obs
 no_meas_maxn_alt AS (
      SELECT
      set_id,
    master_set,
    floor(random() * (2000000 - 1000000 + 1) + 1000000) :: INT AS masterobservation_id,    --insert random numbers to fill ids - make sure they are high enough so they will not be the same as existing ids
    ''::VARCHAR                                  AS "type",    --type
    floor(random() * (2000000 - 1000000 + 1) + 1000000) :: INT AS masterevent_id,
    event_time,
    "value":: VARCHAR,
    0:: INT                               AS measurable_id,                   -- don't need measurable id anymore
    animal_id
      FROM no_meas_maxn
    ),

-- step 5 - then concatenate complete_obs with new table
 complete_obs3 AS (
    WITH all_obs AS (
    SELECT * FROM no_meas_maxn_alt
    UNION
    SELECT * FROM complete_obs
  )
-- step 6 - get rid of false duplication
-- select unique entries per set per animal per time
-- this is necessary bc some sets from complete_obs entered separate observations per individual observed at time=t, but tagged all as having the same maxn
-- eg if maxn=5, there are 5 separate observations indicating maxn=5, each with a different box in the 'image capture' field
  SELECT DISTINCT
    set_id,
    event_time,
    "value",
    animal_id
  FROM all_obs),

--------------------------------------------------------------------------------------------------------
-- now continue to clean maxn data
 maxn AS (
  -- first add zero time, and calculate adjusted time for each event
  WITH em2 AS (
      SELECT
        complete_obs3.set_id,
        complete_obs3.value                               AS maxn,
        complete_obs3.animal_id,
        zero_times.zero_time,
        (complete_obs3.event_time - zero_times.zero_time) AS event_time_adj
      FROM complete_obs3
        LEFT JOIN zero_times
          ON complete_obs3.set_id = zero_times.set_id),
    -- remove events with times over 1 hour, or less than 0
      em3 AS (
        SELECT
          em2.set_id,
          em2.maxn :: INTEGER,
          em2.animal_id,
          em2.event_time_adj,
          text_time(event_time_adj) AS event_time_adj_mins
        FROM em2
        WHERE em2.event_time_adj < 3600001 AND -- 3.6 million milliseconds in an hour
              em2.event_time_adj > 0
    ),
    --select greatest maxn per animal per set
      max_maxn AS (
        SELECT
          max(maxn) AS maxn,
          animal_id,
          set_id
        FROM em3
        GROUP BY animal_id, set_id
    ),
    -- select earliest observation per maxn per animal per set
      em5 AS (
        SELECT
          maxn,
          animal_id,
          set_id,
          min(em3.event_time_adj)      AS min_event_time_milli,
          min(em3.event_time_adj_mins) AS min_event_time_mins
        FROM em3
        GROUP BY maxn, animal_id, set_id)
  --link max maxn (em4) with times from em5
  SELECT
    max_maxn.maxn,
    max_maxn.animal_id,
    max_maxn.set_id,
    em5.min_event_time_mins,
    em5.min_event_time_milli
  FROM max_maxn
    LEFT JOIN em5 ON max_maxn.maxn = em5.maxn AND max_maxn.animal_id = em5.animal_id AND max_maxn.set_id = em5.set_id),

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
  trip_code,
  trip_year,
  reef_name,
  reef_type,
  set_overview.set_code,
  maxn.maxn,
  common_name,
  genus,
  species,
  species_group,
  family,
  maxn.min_event_time_milli AS event_time_mil,
  maxn.min_event_time_mins  AS event_time_mins,
  set_lat,
  set_long,
  visibility,
  depth,
  bait,
  current_flow_estimated,
 current_flow_instrumented,
  set_overview.reef_id,
  set_overview.set_id,
  has_complete_master,
   CASE WHEN (maxn.animal_id IS NULL)
    THEN 9999
  ELSE maxn.animal_id
  END                       AS animal_id
FROM set_overview
  LEFT JOIN maxn ON set_overview.set_id = maxn.set_id
  LEFT JOIN animals ON animals.id = maxn.animal_id;
-- FIN --



