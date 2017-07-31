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
    )
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
    trip_year;



