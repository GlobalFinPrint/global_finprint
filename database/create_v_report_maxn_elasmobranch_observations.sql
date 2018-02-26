--Create view showing maxn values for all sharks and rays, per set, and only using master observations

CREATE OR REPLACE VIEW public.observation_summary AS
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
  bruv_set.id AS set_id,
  bruv_set.code AS set_code,
  bruv_set.latitude AS set_lat,
  bruv_set.longitude AS set_long,
  bruv_set.visibility,
  bruv_set.depth,
  bruv_bait.description AS bait,
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
        AND annotation_masterrecord.status_id = 2),


--Make another table including all observations tagged as being MaxN, and where maxn values are filled in
-- only use master annotations, and of those only complete records
 complete_obs AS (
  SELECT *
  FROM master_obs
  WHERE measurable_id = 2 AND
        value NOT LIKE ''
),

----------------------------------------------------------------------------------------------------------
-- PUT ANOTHER TABLE HERE CALCULATING MAXN WHERE NOT INDICATED IN EVENT MEASURABLES
--step 1 - find sets with no event measurables, but with animals

 master_nomeas AS (
  SELECT *
  FROM master_obs
  WHERE type = 'A' AND measurable_id IS NULL),

-- filter for sets where there are NO event measurables, no maxn are indicated on the video
 master_obs_nomaxn AS (
  WITH maxn_sets AS ( --find all sets that have even one maxn measured:
      SELECT DISTINCT set_id
      FROM complete_obs
      WHERE measurable_id = 2),
      no_meas_sets AS (    --find all sets that ahve even one observation with no measurable
        SELECT DISTINCT set_id
        FROM master_obs
        WHERE measurable_id IS NULL
              AND type = 'A'),
    --take the list of sets with observations missing measurables, and remove any sets that have observations WITH measurables;
      set_select AS (SELECT no_meas_sets.set_id
                     FROM no_meas_sets
                     WHERE set_id NOT IN (
                       SELECT set_id
                       FROM maxn_sets))
  --take these sets with no maxn measurements, and filter all observations out of master_obs
  SELECT *
  FROM master_obs
  WHERE set_id IN (SELECT set_id
                   FROM set_select)
        AND type = 'A'
),


-- make another table of observations for sets where maxn is indicated but no values given
 master_obs_nomaxn2 AS (
  SELECT *
  FROM master_obs
  WHERE measurable_id = 2 AND master_obs.value = ''
),

--put both tables together, then follow the next steps to calculate maxn
  master_obs_nomaxn3 AS (
  SELECT * FROM master_obs_nomaxn
        UNION
        SELECT * FROM master_obs_nomaxn2),

-- aggregate maxn per set per animal per time
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

  -- restructure maxn values with no measurables so they match structure of complete_obs
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

-- then concatenate complete_obs with new table
complete_obs2 AS (
    SELECT * FROM no_meas_maxn_alt
    UNION
    SELECT * FROM complete_obs
  ),

--insert another step where select unique entries per set per animal
 complete_obs3 AS (
  SELECT DISTINCT
    set_id,
    event_time,
    "value",
    animal_id
  FROM complete_obs2),

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

maxnsharks AS (
  SELECT
    maxn,
    animal_id,
    set_id,
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
  set_overview.reef_id,
  trip_code,
  set_overview.set_id,
  set_overview.set_code,
  has_complete_master,
  maxnsharks.maxn,
  CASE WHEN (maxnsharks.animal_id IS NULL)
    THEN 9999
  ELSE maxnsharks.animal_id
  END                       AS animal_id,
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
  bait
FROM set_overview
  LEFT JOIN maxnsharks ON set_overview.set_id = maxnsharks.set_id
  LEFT JOIN animals ON animals.id = maxnsharks.animal_id

);

-- FIN --



