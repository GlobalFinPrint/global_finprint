CREATE OR REPLACE VIEW public.monthly_leaderboard AS
SELECT
  row_number() over () as leaderboard_id,
  u.first_name,
  u.last_name,
  af.name as affiliation_name,
  to_char(asig.last_modified_datetime, 'YYYY-MM'::text) AS month,
  count(asig.id) as num_assignments,
  sum(asig.progress) / 1000 / 60 / 60 as  hours,
  rank()
  OVER (
    PARTITION BY to_char(asig.last_modified_datetime, 'YYYY-MM'::text), af.name
    ORDER BY count(asig.id) DESC )                AS affiliation_count_rank,
  rank()
  OVER (
    PARTITION BY to_char(asig.last_modified_datetime, 'YYYY-MM'::text), af.name
    ORDER BY sum(asig.progress) DESC )                AS affiliation_hour_rank
FROM auth_user u
  INNER JOIN core_finprintuser fp ON fp.user_id = u.id
  INNER JOIN core_affiliation af ON af.id = fp.affiliation_id
  INNER JOIN annotation_assignment asig ON asig.annotator_id = fp.id
WHERE to_char(asig.last_modified_datetime, 'YYYY-MM'::text) IN
      (
        SELECT DISTINCT
          to_char(ml.last_modified_datetime, 'YYYY-MM'::text)
        FROM annotation_assignment ml
        WHERE ml.last_modified_datetime >= now() - INTERVAL '90 days'
      )
      AND af.id NOT IN (0, 1, 7)
      AND asig.status_id IN (3, 4)
GROUP BY
  u.first_name,
  u.last_name,
  af.name,
  to_char(asig.last_modified_datetime, 'YYYY-MM'::text);
