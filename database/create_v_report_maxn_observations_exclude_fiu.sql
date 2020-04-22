--Create view showing maxn values for all sharks and rays, per set, and only using master observations
--Excludes the FIU team's (Team ID 98) data from the results

create OR REPLACE view public.v_report_maxn_observations_exclude_fiu
            (region_name, location_name, site_name, trip_code, trip_year, reef_name, reef_type, set_code, maxn,
             common_name, genus, species, species_group, family, event_time_mil, event_time_mins, set_lat, set_long,
             visibility, depth, bait, current_flow_estimated, current_flow_instrumented, reef_id, set_id, master_set_id,
             animal_id, team_id)
as
WITH set_overview AS (
    WITH so AS (
        SELECT habitat_region.name                                 AS region_name,
               habitat_location.name                               AS location_name,
               habitat_site.name                                   AS site_name,
               habitat_reef.name                                   AS reef_name,
               habitat_reeftype.type                               AS reef_type,
               habitat_reef.id                                     AS reef_id,
               trip_trip.team_id,
               trip_trip.code                                      AS trip_code,
               date_part('year'::text, trip_trip.start_date)::text AS trip_year,
               bruv_set.id                                         AS set_id,
               bruv_set.code                                       AS set_code,
               bruv_set.latitude                                   AS set_lat,
               bruv_set.longitude                                  AS set_long,
               bruv_set.visibility,
               bruv_set.depth,
               bruv_bait.description                               AS bait,
               bruv_set.current_flow_estimated,
               bruv_set.current_flow_instrumented,
               annotation_masterrecord.id                          AS master_set_id,
               CASE
                   WHEN annotation_masterrecord.status_id = 2 THEN 1
                   ELSE 0
                   END                                             AS has_complete_master
        FROM habitat_region
                 FULL JOIN habitat_location ON habitat_region.id = habitat_location.region_id
                 FULL JOIN habitat_site ON habitat_location.id = habitat_site.location_id
                 FULL JOIN habitat_reef ON habitat_site.id = habitat_reef.site_id
                 FULL JOIN habitat_reefhabitat ON habitat_reef.id = habitat_reefhabitat.reef_id
                 FULL JOIN habitat_reeftype ON habitat_reefhabitat.habitat_id = habitat_reeftype.id
                 FULL JOIN bruv_set ON habitat_reefhabitat.id = bruv_set.reef_habitat_id
                 LEFT JOIN trip_trip ON bruv_set.trip_id = trip_trip.id
                 LEFT JOIN annotation_masterrecord ON bruv_set.id = annotation_masterrecord.set_id
                 LEFT JOIN bruv_bait ON bruv_set.bait_id = bruv_bait.id
    )
    SELECT so.region_name,
           so.location_name,
           so.site_name,
           so.reef_name,
           so.reef_type,
           so.reef_id,
           so.team_id,
           so.trip_code,
           so.trip_year,
           so.set_id,
           so.set_code,
           so.set_lat,
           so.set_long,
           so.visibility,
           so.depth,
           so.bait,
           so.current_flow_estimated,
           so.current_flow_instrumented,
           so.master_set_id,
           so.has_complete_master
    FROM so
    WHERE so.set_id IS NOT NULL
),
     master_obs AS (
         SELECT annotation_masterrecord.set_id,
                annotation_masterrecord.id      AS master_set,
                annotation_masterobservation.id AS masterobservation_id,
                annotation_masterobservation.type,
                annotation_masterevent.id       AS masterevent_id,
                annotation_masterevent.event_time,
                CASE
                    WHEN annotation_mastereventmeasurable.value = ''::text OR
                         annotation_mastereventmeasurable.value IS NULL THEN '1'::text
                    ELSE annotation_mastereventmeasurable.value
                    END                         AS value,
                annotation_mastereventmeasurable.measurable_id,
                annotation_masteranimalobservation.animal_id
         FROM annotation_masterrecord
                  LEFT JOIN annotation_masterobservation
                            ON annotation_masterrecord.id = annotation_masterobservation.master_record_id
                  FULL JOIN annotation_masterevent
                            ON annotation_masterobservation.id = annotation_masterevent.master_observation_id
                  LEFT JOIN annotation_mastereventmeasurable
                            ON annotation_masterevent.id = annotation_mastereventmeasurable.master_event_id
                  LEFT JOIN annotation_masteranimalobservation ON annotation_masterobservation.id =
                                                                  annotation_masteranimalobservation.master_observation_id
         WHERE annotation_masterobservation.id IS NOT NULL
           AND annotation_masterrecord.status_id = 2
           AND annotation_masterobservation.type::text = 'A'::text
     ),
     duplicate_records AS (
         SELECT master_obs.set_id,
                master_obs.master_set,
                master_obs.event_time,
                master_obs.animal_id,
                count(master_obs.masterobservation_id)                                  AS num_records,
                max(master_obs.value::integer)                                          AS max_value,
                sum(master_obs.value::integer) / count(master_obs.masterobservation_id) AS value_per_record
         FROM master_obs
         GROUP BY master_obs.set_id, master_obs.master_set, master_obs.event_time, master_obs.animal_id
     ),
     dr2 AS (
         SELECT duplicate_records.set_id,
                duplicate_records.master_set,
                duplicate_records.event_time,
                duplicate_records.animal_id,
                duplicate_records.max_value AS value
         FROM duplicate_records
         WHERE duplicate_records.num_records > 1
           AND duplicate_records.value_per_record > 1
     ),
     master_obs_keep AS (
         SELECT m.set_id,
                m.master_set,
                m.event_time,
                m.animal_id,
                m.value::integer AS value
         FROM master_obs m
                  LEFT JOIN dr2
                            ON m.set_id = dr2.set_id AND m.event_time = dr2.event_time AND m.animal_id = dr2.animal_id
         WHERE dr2.value IS NULL
     ),
     master_obs2 AS (
         SELECT master_obs_keep.set_id,
                master_obs_keep.master_set,
                master_obs_keep.event_time,
                master_obs_keep.animal_id,
                master_obs_keep.value
         FROM master_obs_keep
         UNION ALL
         SELECT dr2.set_id,
                dr2.master_set,
                dr2.event_time,
                dr2.animal_id,
                dr2.value
         FROM dr2
     ),
     master_obs3 AS (
         SELECT master_obs2.set_id,
                master_obs2.master_set,
                master_obs2.event_time,
                master_obs2.animal_id,
                sum(master_obs2.value) AS value
         FROM master_obs2
         GROUP BY master_obs2.set_id, master_obs2.master_set, master_obs2.event_time, master_obs2.animal_id
     ),
     zero_times AS (
         SELECT master_attribute_summary.master_record_id,
                master_attribute_summary.video_id,
                max(
                        CASE
                            WHEN master_attribute_summary.zero_time_tagged = 0 THEN 0
                            ELSE master_attribute_summary.event_time
                            END) AS zero_time
         FROM master_attribute_summary
         GROUP BY master_attribute_summary.master_record_id, master_attribute_summary.video_id
     ),
     maxn AS (
         WITH em2 AS (
             SELECT master_obs3.set_id,
                    master_obs3.master_set,
                    master_obs3.value,
                    master_obs3.animal_id,
                    zero_times.zero_time,
                    master_obs3.event_time - zero_times.zero_time AS event_time_adj
             FROM master_obs3
                      LEFT JOIN zero_times ON master_obs3.master_set = zero_times.master_record_id
         ),
              em3 AS (
                  SELECT em2.set_id,
                         em2.master_set,
                         em2.value,
                         em2.animal_id,
                         em2.event_time_adj,
                         text_time(em2.event_time_adj) AS event_time_adj_mins
                  FROM em2
                  WHERE em2.event_time_adj < 3600001
                    AND em2.event_time_adj > 0
              ),
              max_maxn AS (
                  SELECT max(em3.value) AS maxn,
                         em3.animal_id,
                         em3.set_id,
                         em3.master_set
                  FROM em3
                  GROUP BY em3.animal_id, em3.set_id, em3.master_set
              ),
              em5 AS (
                  SELECT em3.value,
                         em3.animal_id,
                         em3.set_id,
                         em3.master_set,
                         min(em3.event_time_adj)      AS min_event_time_milli,
                         min(em3.event_time_adj_mins) AS min_event_time_mins
                  FROM em3
                  GROUP BY em3.value, em3.animal_id, em3.set_id, em3.master_set
              )
         SELECT max_maxn.maxn,
                max_maxn.animal_id,
                max_maxn.set_id,
                max_maxn.master_set,
                em5.min_event_time_mins,
                em5.min_event_time_milli
         FROM max_maxn
                  LEFT JOIN em5 ON max_maxn.maxn = em5.value AND max_maxn.animal_id = em5.animal_id AND
                                   max_maxn.set_id = em5.set_id AND max_maxn.master_set = em5.master_set
     ),
     animals AS (
         SELECT annotation_animal.id,
                annotation_animal.common_name,
                annotation_animal.genus,
                annotation_animal.species,
                annotation_animal.family,
                annotation_animalgroup.name AS species_group
         FROM annotation_animal
                  LEFT JOIN annotation_animalgroup ON annotation_animal.group_id = annotation_animalgroup.id
     )
SELECT set_overview.region_name,
       set_overview.location_name,
       set_overview.site_name,
       set_overview.trip_code,
       set_overview.trip_year,
       set_overview.reef_name,
       set_overview.reef_type,
       set_overview.set_code,
       maxn.maxn,
       animals.common_name,
       animals.genus,
       animals.species,
       animals.species_group,
       animals.family,
       maxn.min_event_time_milli AS event_time_mil,
       maxn.min_event_time_mins  AS event_time_mins,
       set_overview.set_lat,
       set_overview.set_long,
       set_overview.visibility,
       set_overview.depth,
       set_overview.bait,
       set_overview.current_flow_estimated,
       set_overview.current_flow_instrumented,
       set_overview.reef_id,
       set_overview.set_id,
       set_overview.master_set_id,
       CASE
           WHEN maxn.animal_id IS NULL THEN 9999
           ELSE maxn.animal_id
           END                   AS animal_id,
       set_overview.team_id
FROM set_overview
         LEFT JOIN maxn ON set_overview.set_id = maxn.set_id AND set_overview.master_set_id = maxn.master_set
         LEFT JOIN animals ON animals.id = maxn.animal_id
WHERE set_overview.has_complete_master = 1
  AND set_overview.team_id <> 98;

alter table v_report_maxn_observations_exclude_fiu
    owner to finprint;

