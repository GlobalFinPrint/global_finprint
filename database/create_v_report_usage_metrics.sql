-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_usage_metrics AS
  WITH legacy_videos AS (
      SELECT av.id
      FROM annotation_video av
        JOIN annotation_assignment aa ON (av.id = aa.video_id)
        JOIN annotation_observation ao ON (aa.id = ao.assignment_id)
        JOIN annotation_event ae ON (ao.id = ae.observation_id)
      WHERE ae.raw_import_json IS NOT NULL)
  SELECT
    'Total videos watched' AS metric,
    count(1)               AS value
  FROM annotation_assignment
  WHERE progress > 0 AND status_id > 2 AND video_id NOT IN (SELECT id
                                                            FROM legacy_videos)
  UNION
  SELECT
    'Total unique videos watched' AS metric,
    count(1)                      AS value
  FROM (
         SELECT DISTINCT video_id
         FROM annotation_assignment
         WHERE progress > 0 AND status_id > 2 AND video_id NOT IN (SELECT id
                                                                   FROM legacy_videos)
       ) temp
  UNION
  SELECT
    'Total hours of video watched' AS metric,
    sum(progress) / 1000 / 60 / 60 AS value
  FROM annotation_assignment
  WHERE progress > 0 AND status_id > 0 AND video_id NOT IN (SELECT id
                                                            FROM legacy_videos)
  UNION
  SELECT
    'Unique users that have watched videos' AS metric,
    count(1)                                AS value
  FROM (
         SELECT DISTINCT annotator_id
         FROM annotation_assignment
         WHERE progress > 0 AND status_id > 0 AND video_id NOT IN (SELECT id
                                                                   FROM legacy_videos)
       ) temp
  UNION
  SELECT
    'Total observations recorded' AS metric,
    count(1)                      AS value
  FROM annotation_observation ao
    JOIN annotation_assignment aa ON (aa.id = ao.assignment_id)
  WHERE aa.progress > 0 AND aa.status_id > 0 AND aa.video_id NOT IN (SELECT id
                                                                     FROM legacy_videos)
  UNION
  SELECT
    'Total events recorded' AS metric,
    count(1)                AS value
  FROM annotation_event ae
    JOIN annotation_observation ao ON (ao.id = ae.observation_id)
    JOIN annotation_assignment aa ON (aa.id = ao.assignment_id)
  WHERE aa.progress > 0 AND aa.status_id > 0 AND aa.video_id NOT IN (SELECT id
                                                                     FROM legacy_videos)
  UNION
  SELECT
    'Number of videos started but not completed' AS metric,
    count(1)                                     AS value
  FROM annotation_assignment
  WHERE progress > 0 AND status_id = 1 AND video_id NOT IN (SELECT id
                                                            FROM legacy_videos)
  UNION
  SELECT
    'Total number of videos' AS metric,
    count(1)                 AS value
  FROM annotation_video
  WHERE id NOT IN (SELECT id
                   FROM legacy_videos);
