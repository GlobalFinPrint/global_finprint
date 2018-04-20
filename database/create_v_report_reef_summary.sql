/* Summary of data completeness of all reefs, including reef level metadata */

CREATE OR REPLACE VIEW public.v_report_reef_summary AS
  WITH assignment_status_summary AS
  (
      SELECT DISTINCT
        s.id         AS set_id,
        assig.video_id,
        assigst.id   AS assignment_status_id,
        assigst.name AS assignment_status,
        count(*)     AS status_count
      FROM
        bruv_set s
        INNER JOIN annotation_assignment assig ON assig.video_id = s.video_id
        INNER JOIN annotation_annotationstate assigst ON assigst.id = assig.status_id
      GROUP BY
        s.id,
        assig.video_id,
        assigst.id,
        assigst.name
  ),
    set_summary AS (
        SELECT
          s.trip_id,
          s.id AS set_id,
          s.reef_habitat_id,
          habitat_reefhabitat.reef_id,
          CASE
          WHEN SUM(assstat.status_count) filter (where assstat.assignment_status_id = 3 OR assstat.assignment_status_id = 4) >= 1
            THEN 1
          ELSE 0
          END  AS min_1_complete_annotation,
          CASE
          WHEN mas.id IS NOT NULL
            THEN 1
          ELSE 0
          END  AS has_complete_master,
          CASE
          WHEN
            S.visibility IS NOT NULL
            AND (S.current_flow_estimated IS NOT NULL
                 OR S.current_flow_instrumented IS NOT NULL)
            AND sub.type IS NOT NULL  --substrate type
            AND subc.name IS NOT NULL --substrate complexity
            AND S.bait_id IS NOT NULL
            AND (S.latitude!=0 AND S.longitude!=0)
            THEN 1
          ELSE 0
          END  AS has_all_set_metadata
        FROM trip_trip t
          INNER JOIN bruv_set S ON S.trip_id = t.id
          LEFT JOIN habitat_substrate sub ON sub.id = S.substrate_id
          LEFT JOIN habitat_substratecomplexity subc ON subc.id = S.substrate_complexity_id
          LEFT JOIN annotation_video v ON v.id = S.video_id
          LEFT JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)
          LEFT JOIN annotation_masterrecord mas ON (mas.set_id = S.id
                                                    AND mas.status_id = 2)
          LEFT JOIN assignment_status_summary assstat ON assstat.video_id = v.id
          LEFT JOIN habitat_reefhabitat ON S.reef_habitat_id=habitat_reefhabitat.id
        GROUP BY
          S.trip_id,
          S.id,
          S.reef_habitat_id,
          habitat_reefhabitat.reef_id,
          has_complete_master,
          has_all_set_metadata
    ),

    set_summary_agg AS (
  SELECT
      trip_id,
      reef_id,
      count(distinct set_id)    AS num_sets,
sum(min_1_complete_annotation)    AS have_min_1_complete_annotation,
sum(has_complete_master)          AS have_complete_master,
sum(has_all_set_metadata)         AS have_all_set_metadata
      FROM set_summary
      GROUP BY reef_id,
      trip_id
    ),

    habitat_summary AS (
        SELECT DISTINCT
          extract(YEAR FROM t.start_date) :: TEXT AS trip_year,
          t.code                                  AS trip_code,
          t.id                                    AS trip_id,
          hab.region_name                         AS region_name,
          hab.location_name                       AS location_name,
          hab.site_name                           AS site_name,
          hab.reef_name                           AS reef_name,
          hab.region_id,
          hab.location_id,
          hab.site_id,
          hab.reef_id
        FROM
          trip_trip t
          INNER JOIN habitat_summary hab ON hab.location_id = t.location_id
    ),


reef_metadata AS (
  /* this script makes a summary table showing all reef-level metadata, e.g. levels of fishing and compliance with MPAs */
    SELECT
      habitat_reef.id                                    AS reef_id,
      /* reef_ID acts as primary key for this table*/
      habitat_protectionstatus.type                      AS protection_status,
      habitat_mpa.name                                   AS MPA_name,
      habitat_mpa.area                                   AS MPA_area,
      habitat_mpa.founded                                AS MPA_year_founded,
      habitat_mpaisolation.type                          AS MPA_isolation,
      habitat_mpacompliance.type                         AS MPA_compliance,

      string_agg(habitat_fishingrestrictions.type,
                 ', ')                                   AS fishing_restrictions /* each reef can have multiple types of fishing restrictions */
    FROM habitat_reef
      LEFT JOIN habitat_protectionstatus ON habitat_reef.protection_status_id = habitat_protectionstatus.id
      LEFT JOIN habitat_mpa ON habitat_reef.mpa_id = habitat_mpa.id
      LEFT JOIN habitat_mpaisolation ON habitat_mpa.mpa_isolation_id = habitat_mpaisolation.id
      LEFT JOIN habitat_mpacompliance ON habitat_mpa.mpa_compliance_id = habitat_mpacompliance.id
      LEFT JOIN habitat_reef_fishing_restrictions ON habitat_reef.id = habitat_reef_fishing_restrictions.reef_id
      LEFT JOIN habitat_fishingrestrictions
        ON habitat_reef_fishing_restrictions.fishingrestrictions_id = habitat_fishingrestrictions.id
    GROUP BY
      habitat_reef.id,
      habitat_reef.name,
      habitat_protectionstatus.type,
      habitat_mpa.name,
      habitat_mpa.area,
      habitat_mpa.founded,
      habitat_mpaisolation.type,
      habitat_mpacompliance.type
),


    fishing_metadata AS (
      SELECT
        habitat_reef.id                               AS reef_id,
        string_agg(habitat_sharkgearinuse.type, '; ') AS shark_fishing_gear /* each reef can have multiple fishing gears */
      FROM habitat_reef
        LEFT JOIN habitat_reef_shark_gear_in_use ON habitat_reef.id = habitat_reef_shark_gear_in_use.reef_id
        LEFT JOIN habitat_sharkgearinuse ON habitat_reef_shark_gear_in_use.sharkgearinuse_id = habitat_sharkgearinuse.id
      GROUP BY habitat_reef.id
  )


SELECT
region_name,
location_name,
site_name,
reef_name,
trip_year,
trip_code,
  CASE WHEN
    num_sets IS NULL THEN 0
    ELSE num_sets
      END AS num_sets,
  CASE WHEN have_min_1_complete_annotation IS NULL
    THEN 0
      ELSE have_min_1_complete_annotation
        END AS have_min_1_complete_annotation,
  CASE WHEN have_complete_master IS NULL
    THEN 0
      ELSE have_complete_master
        END AS have_complete_master,
  CASE WHEN have_all_set_metadata IS NULL
    THEN 0
      ELSE have_all_set_metadata
        END AS have_all_set_metadata,
protection_status,
mpa_name,
  mpa_area,
  mpa_year_founded,
  mpa_isolation,
  mpa_compliance,
  fishing_restrictions,
  shark_fishing_gear,
region_id,
location_id,
habitat_summary.trip_id
site_id,
habitat_summary.reef_id
  FROM habitat_summary
       LEFT JOIN set_summary_agg ON set_summary_agg.reef_id=habitat_summary.reef_id
                             AND   set_summary_agg.trip_id=habitat_summary.trip_id
    LEFT JOIN reef_metadata ON reef_metadata.reef_id=habitat_summary.reef_id
    LEFT JOIN fishing_metadata ON fishing_metadata.reef_id=habitat_summary.reef_id

 ;