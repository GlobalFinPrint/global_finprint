CREATE OR REPLACE VIEW public.v_report_assignment_status_by_file AS
WITH not_started_assignments AS
(
    SELECT
      v.id         AS video_id,
      count(aa.id) AS assignment_count
    FROM annotation_video v
      INNER JOIN annotation_assignment aa ON aa.video_id = v.id
    WHERE aa.status_id = 1
    GROUP BY v.id
    HAVING count(aa.id) > 0
),
    in_progress_assignments AS
  (
      SELECT
        v.id         AS video_id,
        count(aa.id) AS assignment_count
      FROM annotation_video v
        INNER JOIN annotation_assignment aa ON aa.video_id = v.id
      WHERE aa.status_id = 2
      GROUP BY v.id
      HAVING count(aa.id) > 0
  ),
    ready_for_review_assignments AS
  (
      SELECT
        v.id         AS video_id,
        count(aa.id) AS assignment_count
      FROM annotation_video v
        INNER JOIN annotation_assignment aa ON aa.video_id = v.id
      WHERE aa.status_id = 3
      GROUP BY v.id
      HAVING count(aa.id) > 0
  ),
    completed_assignments AS
  (
      SELECT
        v.id         AS video_id,
        count(aa.id) AS assignment_count
      FROM annotation_video v
        INNER JOIN annotation_assignment aa ON aa.video_id = v.id
      WHERE aa.status_id = 4
      GROUP BY v.id
      HAVING count(aa.id) > 0
  )
SELECT
  tm.sampler_collaborator as team,
  t.code || '_' || s.code           AS code,
  vf.file                           AS primary_video_file_name,
  vf.source                         AS video_source,
  vf.path                           AS video_path,
  coalesce(aa.assignment_count, 0)  AS not_started,
  coalesce(ipa.assignment_count, 0) AS in_progress,
  coalesce(ra.assignment_count, 0)  AS ready_for_review,
  coalesce(ca.assignment_count, 0)  AS complete
FROM
  core_team tm
  inner join trip_trip t on t.team_id = tm.id
  INNER JOIN bruv_set s ON s.trip_id = t.id
  LEFT JOIN annotation_video v ON v.id = s.video_id
  LEFT JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)
  LEFT JOIN not_started_assignments aa ON aa.video_id = s.video_id
  LEFT JOIN in_progress_assignments ipa ON ipa.video_id = s.video_id
  LEFT JOIN ready_for_review_assignments ra ON ra.video_id = s.video_id
  LEFT JOIN completed_assignments ca ON ca.video_id = s.video_id
ORDER BY t.code || '_' || s.code;
