-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_usage_metrics_by_affiliation AS
WITH legacy_videos AS (
    SELECT av.id
    FROM annotation_video av
      JOIN annotation_assignment aa ON (av.id = aa.video_id)
      JOIN annotation_observation ao ON (aa.id = ao.assignment_id)
      JOIN annotation_event ae ON (ao.id = ae.observation_id)
    WHERE ae.raw_import_json IS NOT NULL)
SELECT
  'Total videos watched - ' || ca.name AS metric,
  count(1)                             AS value
FROM annotation_assignment aa
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE progress > 0 AND status_id > 2
      AND video_id NOT IN (SELECT id
                           FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Total unique videos watched - ' || name AS metric,
  count(1)                                 AS value
FROM (
       SELECT DISTINCT
         video_id,
         ca.name
       FROM annotation_assignment aa
         JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
         JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
       WHERE progress > 0 AND status_id > 2
             AND video_id NOT IN (SELECT id
                                  FROM legacy_videos)
     ) temp
GROUP BY name
UNION
SELECT
  'Total hours of video watched - ' || ca.name AS metric,
  sum(progress) / 1000 / 60 / 60               AS value
FROM annotation_assignment aa
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE progress > 0 AND status_id > 0
      AND video_id NOT IN (SELECT id
                           FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Unique users that have watched videos - ' || name AS metric,
  count(1)                                           AS value
FROM (
       SELECT DISTINCT
         annotator_id,
         ca.name
       FROM annotation_assignment aa
         JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
         JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
       WHERE progress > 0 AND status_id > 0
             AND video_id NOT IN (SELECT id
                                  FROM legacy_videos)
     ) temp
GROUP BY name
UNION
SELECT
  'Total observations recorded - ' || ca.name AS metric,
  count(1)                                    AS value
FROM annotation_observation ao
  JOIN annotation_assignment aa ON (aa.id = ao.assignment_id)
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE aa.progress > 0 AND aa.status_id > 0
      AND aa.video_id NOT IN (SELECT id
                              FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Total events recorded - ' || ca.name AS metric,
  count(1)                              AS value
FROM annotation_event ae
  JOIN annotation_observation ao ON (ao.id = ae.observation_id)
  JOIN annotation_assignment aa ON (aa.id = ao.assignment_id)
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE aa.progress > 0 AND aa.status_id > 0
      AND aa.video_id NOT IN (SELECT id
                              FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Number of videos started but not completed - ' || ca.name AS metric,
  count(1)                                                   AS value
FROM annotation_assignment aa
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE progress > 0 AND status_id = 1
      AND video_id NOT IN (SELECT id
                           FROM legacy_videos)
GROUP BY ca.name
ORDER BY metric;
