-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_usage_metrics AS
  SELECT 'Total videos watched' as metric, count(1) as value
  FROM annotation_assignment
  WHERE progress > 0 AND status_id > 2
  UNION
  SELECT 'Total unique videos watched' as metric, count(1) AS value
  FROM (
         SELECT DISTINCT video_id
         FROM annotation_assignment
         WHERE progress > 0 AND status_id > 2
       ) temp
  UNION
  SELECT 'Total hours of video watched' as metric, sum(progress) / 1000 / 60 / 60 AS value
  FROM annotation_assignment
  WHERE progress > 0 AND status_id > 0
  union
  SELECT 'Unique users that have watched videos' as metric, count(1) AS value
  FROM (
         SELECT DISTINCT annotator_id
         FROM annotation_assignment
         WHERE progress > 0 AND status_id > 0
       ) temp
  UNION
  SELECT 'Total observations recorded' as metric, count(1) AS value
  FROM annotation_observation ao
    JOIN annotation_assignment aa ON (aa.id = ao.assignment_id)
  WHERE aa.progress > 0 AND aa.status_id > 0
  UNION
  SELECT 'Total events recorded' as metric, count(1) AS value
  FROM annotation_event ae
    JOIN annotation_observation ao ON (ao.id = ae.observation_id)
    JOIN annotation_assignment aa ON (aa.id = ao.assignment_id)
  WHERE aa.progress > 0 AND aa.status_id > 0
  UNION
  SELECT 'Number of videos started but not completed' as metric, count(1) AS value
  FROM annotation_assignment
  WHERE progress > 0 AND status_id = 1
  UNION
  SELECT 'Total number of videos' as metric, count(1) as value
  FROM annotation_video;
