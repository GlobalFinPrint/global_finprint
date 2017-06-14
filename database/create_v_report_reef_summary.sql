CREATE OR REPLACE VIEW public.v_report_reef_summary AS
WITH assignment_status_summary AS
(
    SELECT
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
    set_summary AS
  (
      SELECT
        s.trip_id,
        s.id AS set_id,
        s.reef_habitat_id,
        CASE
        WHEN coalesce(assstatcom.status_count, 0) >= 2
          THEN 1
        ELSE 0
        END  AS has_two_complete_annotations,
        CASE
        WHEN coalesce(assstatrev.status_count, 0) >= 2
          THEN 1
        ELSE 0
        END  AS has_two_reviewed_annotations,
        CASE
        WHEN mas.id IS NOT NULL
          THEN 1
        ELSE 0
        END  AS has_complete_master,
        CASE
        WHEN
          s.visibility IS NOT NULL
          AND (s.current_flow_estimated IS NOT NULL
               OR s.current_flow_instrumented IS NOT NULL)
          AND sub.type IS NOT NULL
          AND subc.name IS NOT NULL
          THEN 1
        ELSE 0
        END  AS has_all_fields,
        CASE
        WHEN mas.id IS NOT NULL
             AND s.visibility IS NOT NULL
             AND (s.current_flow_estimated IS NOT NULL
                  OR s.current_flow_instrumented IS NOT NULL)
             AND sub.type IS NOT NULL
             AND subc.name IS NOT NULL
          THEN 1
        ELSE 0
        END  AS set_complete
      FROM trip_trip t
        INNER JOIN bruv_set s ON s.trip_id = t.id
        LEFT JOIN habitat_substrate sub ON sub.id = s.substrate_id
        LEFT JOIN habitat_substratecomplexity subc ON subc.id = s.substrate_complexity_id
        LEFT JOIN annotation_video v ON v.id = s.video_id
        LEFT JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)
        LEFT JOIN annotation_masterrecord mas ON (mas.set_id = s.id
                                                  AND mas.status_id = 2)
        LEFT JOIN assignment_status_summary assstatcom ON (assstatcom.video_id = v.id
                                                           AND assstatcom.assignment_status_id = 3)
        LEFT JOIN assignment_status_summary assstatrev ON (assstatrev.video_id = v.id
                                                           AND assstatrev.assignment_status_id IN (4, 5, 6))
  ),
    total_assignments AS
  (
      SELECT
        set_id,
        sum(status_count) AS total
      FROM assignment_status_summary
      GROUP BY set_id
  )
SELECT
  extract(YEAR FROM t.start_date)     AS trip_year,
  hab.region,
  hab.location,
  hab.site,
  hab.reef,

  count(s.set_id)                     AS count_of_sets,
  sum(coalesce(tot.total, 0))         AS total_assignments,
  sum(s.has_two_complete_annotations) AS have_two_complete_assignments,
  sum(s.has_two_reviewed_annotations) AS have_two_reviewed_assignments,
  sum(s.has_complete_master)          AS have_complete_master,
  sum(s.has_all_fields)               AS have_all_set_fields,
  sum(s.set_complete)                 AS complete_sets,

  hab.region_id,
  hab.location_id,
  hab.site_id,
  hab.reef_id
FROM
  trip_trip t
  INNER JOIN set_summary s ON s.trip_id = t.id
  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = s.reef_habitat_id
  LEFT JOIN total_assignments tot ON tot.set_id = s.set_id
GROUP BY
  trip_year,
  hab.region,
  hab.location,
  hab.site,
  hab.reef,
  hab.region_id,
  hab.location_id,
  hab.site_id,
  hab.reef_id
ORDER BY
  hab.region,
  hab.location,
  hab.site,
  hab.reef,
  trip_year;

