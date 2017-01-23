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
  'Total videos watched' AS metric,
  ca.name                AS affiliation,
  count(1)               AS value
FROM annotation_assignment aa
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE progress > 0 AND status_id > 2
      AND video_id NOT IN (SELECT id FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Total unique videos watched' AS metric,
  name                          AS affiliation,
  count(1)                      AS value
FROM (
       SELECT DISTINCT
         video_id,
         ca.name
       FROM annotation_assignment aa
         JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
         JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
       WHERE progress > 0 AND status_id > 2
             AND video_id NOT IN (SELECT id FROM legacy_videos)
     ) temp
GROUP BY name
UNION
SELECT
  'Total hours of video watched' AS metric,
  ca.name                        AS affiliation,
  sum(progress) / 1000 / 60 / 60 AS value
FROM annotation_assignment aa
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE progress > 0 AND video_id NOT IN (SELECT id FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Unique users that have watched videos' AS metric,
  name                                    AS affiliation,
  count(1)                                AS value
FROM (
       SELECT DISTINCT
         annotator_id,
         ca.name
       FROM annotation_assignment aa
         JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
         JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
       WHERE progress > 0 AND video_id NOT IN (SELECT id FROM legacy_videos)
     ) temp
GROUP BY name
UNION
SELECT
  'Total observations recorded' AS metric,
  ca.name                       AS affiliation,
  count(1)                      AS value
FROM annotation_observation ao
  JOIN annotation_assignment aa ON (aa.id = ao.assignment_id)
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE aa.progress > 0 AND aa.video_id NOT IN (SELECT id FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Total events recorded' AS metric,
  ca.name                 AS affiliation,
  count(1)                AS value
FROM annotation_event ae
  JOIN annotation_observation ao ON (ao.id = ae.observation_id)
  JOIN annotation_assignment aa ON (aa.id = ao.assignment_id)
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE aa.progress > 0 AND aa.video_id NOT IN (SELECT id FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Number of videos started but not completed' AS metric,
  ca.name                                      AS affiliation,
  count(1)                                     AS value
FROM annotation_assignment aa
  JOIN core_finprintuser cf ON (aa.annotator_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE progress > 0 AND status_id = 2 AND video_id NOT IN (SELECT id FROM legacy_videos)
GROUP BY ca.name
UNION
SELECT
  'Total number of videos' AS metric,
  ca.name                  AS affiliation,
  count(1)                 AS value
FROM annotation_video av
  JOIN bruv_set bs ON (bs.video_id = av.id)
  JOIN trip_trip tt ON (bs.trip_id = tt.id)
  JOIN core_team ct ON (tt.team_id = ct.id)
  JOIN core_finprintuser cf ON (ct.lead_id = cf.id)
  JOIN core_affiliation ca ON (cf.affiliation_id = ca.id)
WHERE av.id NOT IN (SELECT id FROM legacy_videos)
GROUP BY ca.name
ORDER BY metric;
