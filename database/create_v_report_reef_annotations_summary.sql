/* Summary of  completeness of annotations for all reefs */

CREATE OR REPLACE VIEW public.v_report_reef_annotations_summary AS
/* Summary of  completeness of annotations for all reefs */
    WITH assignment_status_summary AS
  (
      SELECT DISTINCT
        s.id         AS set_id,
        assigst.id   AS assignment_status_id,
        assigst.name AS assignment_status,
        count(*)     AS status_count
      FROM
        bruv_set s
        INNER JOIN annotation_assignment assig ON assig.video_id = s.video_id
        INNER JOIN annotation_annotationstate assigst ON assigst.id = assig.status_id
      GROUP BY
        s.id,
        assigst.id,
        assigst.name
  ),
    set_summary AS (
        SELECT
          extract(YEAR FROM t.start_date) :: TEXT AS trip_year,
          t.code                                  AS trip_code,
          s.trip_id,
          s.id AS set_id,
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
          END  AS has_complete_master
        FROM trip_trip t
          INNER JOIN bruv_set S ON S.trip_id = t.id
            LEFT JOIN annotation_masterrecord mas ON (mas.set_id = S.id
                                                    AND mas.status_id = 2)
          LEFT JOIN assignment_status_summary assstat ON assstat.set_id = S.id
          LEFT JOIN habitat_reefhabitat ON S.reef_habitat_id=habitat_reefhabitat.id
        GROUP BY
          S.trip_id,
          t.code,
          t.start_date,
          S.id,
          S.reef_habitat_id,
          habitat_reefhabitat.reef_id,
          has_complete_master
   ),

   set_summary_agg AS (
  SELECT
      trip_year,
    trip_code,
    trip_id,
      reef_id,
      count(distinct set_id)    AS num_sets,
sum(min_1_complete_annotation)    AS have_min_1_complete_annotation,
sum(has_complete_master)          AS have_complete_master
      FROM set_summary
      GROUP BY reef_id,
      trip_id,
        trip_code,
        trip_year
   ),

   habitat_summary AS (
        SELECT DISTINCT
          habitat_region.name                         AS region_name,
          habitat_location.name                       AS location_name,
          habitat_site.name                           AS site_name,
          habitat_site.type                           AS site_type,
          habitat_reef.name                           AS reef_name,
          habitat_region.id                       AS region_id,
          habitat_location.id                     AS location_id,
          habitat_site.id                         AS site_id,
          habitat_reef.id                         AS reef_id
        FROM habitat_region
          LEFT JOIN habitat_location ON habitat_region.id=habitat_location.region_id
          LEFT JOIN habitat_site ON habitat_location.id=habitat_site.location_id
          LEFT JOIN habitat_reef ON habitat_site.id=habitat_reef.site_id
          LEFT JOIN habitat_reefhabitat ON habitat_reef.id=habitat_reefhabitat.reef_id
     WHERE habitat_reef.id IS NOT NULL
    )

SELECT DISTINCT
region_name,
location_name,
site_name,
site_type,
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
region_id,
location_id,
set_summary_agg.trip_id,
habitat_summary.site_id,
habitat_summary.reef_id
  FROM habitat_summary
       LEFT JOIN set_summary_agg ON set_summary_agg.reef_id=habitat_summary.reef_id
 ;



