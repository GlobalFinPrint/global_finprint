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
          CASE
          WHEN sum(COALESCE(assstat.status_count, 0)) >= 1
            THEN 1
          ELSE 0
          END  AS has_assignments,
          CASE
          WHEN (
                 SELECT sum(assstatcom.status_count)
                 FROM assignment_status_summary assstatcom
                 WHERE assstatcom.assignment_status_id IN (3, 4, 5, 6)
                       AND assstatcom.set_id = S.id
               ) >= 2
            THEN 1
          ELSE 0
          END  AS has_two_complete_assignments,
          CASE
          WHEN (
                 SELECT sum(assstatcom.status_count)
                 FROM assignment_status_summary assstatcom
                 WHERE assstatcom.assignment_status_id IN (4, 5, 6)
                       AND assstatcom.set_id = S.id
               ) >= 2
            THEN 1
          ELSE 0
          END  AS has_two_reviewed_assignments,
          CASE
          WHEN
            (sum(COALESCE(assstat.status_count, 0)) = 1)
              AND
              (
                 SELECT sum(assstatcom.status_count)
                 FROM assignment_status_summary assstatcom
                 WHERE assstatcom.assignment_status_id IN (4, 5, 6)
                       AND assstatcom.set_id = S.id
               ) = 1
            THEN 1
          ELSE 0
          END  AS one_assignment_one_reviewed,
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
            AND sub.type IS NOT NULL
            AND subc.name IS NOT NULL
            THEN 1
          ELSE 0
          END  AS has_all_fields,
          CASE
          WHEN mas.id IS NOT NULL
               AND S.visibility IS NOT NULL
               AND (S.current_flow_estimated IS NOT NULL
                    OR S.current_flow_instrumented IS NOT NULL)
               AND sub.type IS NOT NULL
               AND subc.name IS NOT NULL
            THEN 1
          ELSE 0
          END  AS set_complete
        FROM trip_trip t
          INNER JOIN bruv_set S ON S.trip_id = t.id
          LEFT JOIN habitat_substrate sub ON sub.id = S.substrate_id
          LEFT JOIN habitat_substratecomplexity subc ON subc.id = S.substrate_complexity_id
          LEFT JOIN annotation_video v ON v.id = S.video_id
          LEFT JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)
          LEFT JOIN annotation_masterrecord mas ON (mas.set_id = S.id
                                                    AND mas.status_id = 2)
          LEFT JOIN assignment_status_summary assstat ON assstat.video_id = v.id
        GROUP BY
          S.trip_id,
          S.id,
          S.reef_habitat_id,
          has_complete_master,
          has_all_fields,
          set_complete
    ),
    annotation_summary AS (
  SELECT
    extract(YEAR FROM t.start_date) :: TEXT AS trip_year,
    hab.region_name                         AS region_name,
    hab.location_name                       AS location_name,
    hab.site_name                           AS site_name,
    hab.reef_name                           AS reef_name,

    count(DISTINCT s.set_id)                AS count_of_sets,
    sum(s.has_assignments)                  AS with_assignments,
    sum(s.has_two_complete_assignments)     AS have_two_complete_assignments,
    sum(s.has_two_reviewed_assignments)     AS have_two_reviewed_assignments,
    sum(s.one_assignment_one_reviewed)      AS have_one_assignment_and_one_reviewed,
    sum(s.has_complete_master)              AS have_complete_master,
    sum(s.has_all_fields)                   AS have_all_set_fields,
    sum(s.set_complete)                     AS complete_sets,

    hab.region_id,
    hab.location_id,
    hab.site_id,
    hab.reef_id
  FROM
    trip_trip t
    INNER JOIN set_summary s ON s.trip_id = t.id
    INNER JOIN habitat_summary hab ON hab.reef_habitat_id = s.reef_habitat_id
  GROUP BY
    trip_year,
    hab.region_name,
    hab.location_name,
    hab.site_name,
    hab.reef_name,
    hab.region_id,
    hab.location_id,
    hab.site_id,
    hab.reef_id
  ORDER BY
    hab.region_name,
    hab.location_name,
    hab.site_name,
    hab.reef_name,
    trip_year),


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
count_of_sets,
with_assignments,
have_two_complete_assignments,
have_two_reviewed_assignments,
have_one_assignment_and_one_reviewed,
have_complete_master,
have_all_set_fields,
protection_status,
mpa_name,
mpa_area,
MPA_year_founded,
MPA_isolation,
MPA_compliance,
fishing_restrictions,
shark_fishing_gear,
region_id,
location_id,
site_id,
annotation_summary.reef_id
FROM
annotation_summary
LEFT JOIN reef_metadata ON annotation_summary.reef_id=reef_metadata.reef_id
LEFT JOIN fishing_metadata ON annotation_summary.reef_id=fishing_metadata.reef_id;




