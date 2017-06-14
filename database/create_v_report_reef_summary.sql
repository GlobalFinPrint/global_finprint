CREATE OR REPLACE VIEW public.v_report_reef_summary AS
WITH assignment_status_summary AS
(
    SELECT
      assig.video_id,
      assigst.id   AS assignment_status_id,
      assigst.name AS assignment_status,
      count(*)     AS status_count
    FROM annotation_assignment assig
      INNER JOIN annotation_annotationstate assigst ON assigst.id = assig.status_id
    GROUP BY assig.video_id,
      assigst.id,
      assigst.name
),
    set_summary AS
  (
      SELECT
        s.id,
        s.reef_habitat_id,
        CASE
        WHEN coalesce(assstat.status_count, 0) >= 2
          THEN 1
        ELSE 0
        END AS has_two_annotations,
        CASE
        WHEN mas.id IS NOT NULL
          THEN 1
        ELSE 0
        END AS has_complete_master,
        CASE
        WHEN
          s.visibility IS NOT NULL
          AND (s.current_flow_estimated IS NOT NULL
               OR s.current_flow_instrumented IS NOT NULL)
          AND sub.type IS NOT NULL
          AND subc.name IS NULL
          THEN 1
        ELSE 0
        END AS has_all_fields
      FROM bruv_set s
        LEFT JOIN habitat_substrate sub ON sub.id = s.substrate_id
        LEFT JOIN habitat_substratecomplexity subc ON subc.id = s.substrate_complexity_id
        LEFT JOIN annotation_video v ON v.id = s.video_id
        LEFT JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)
        LEFT JOIN annotation_masterrecord mas ON (mas.set_id = s.id
                                                  AND mas.status_id = 2)
        LEFT JOIN assignment_status_summary assstat ON (assstat.video_id = v.id
                                                        AND assstat.assignment_status_id = 4)
  )
SELECT
  hab.region,
  hab.location,
  hab.site,
  hab.reef,

  count(s.id)                AS count_of_sets,
  sum(s.has_two_annotations) AS have_two_complete_annotations,
  sum(s.has_complete_master) AS have_complete_master,
  sum(s.has_all_fields)      AS have_all_fields,

  hab.region_id,
  hab.location_id,
  hab.site_id,
  hab.reef_id
FROM
  set_summary s
  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = s.reef_habitat_id
GROUP BY
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
  hab.reef;
