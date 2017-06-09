CREATE OR REPLACE VIEW public.overall_leaderboard AS
SELECT
  aff.name AS affiliation,
  u.first_name,
  u.last_name,
  count(a.id)
FROM annotation_assignment a
  INNER JOIN core_finprintuser an ON an.id = a.annotator_id
  INNER JOIN auth_user u ON u.id = an.user_id
  INNER JOIN core_affiliation aff ON aff.id = an.affiliation_id
WHERE a.status_id in (3, 4) -- on 'ready ..' and 'reviewed'
  and aff.id not in (0, 1, 7) -- not 'noo affiliation', 'test' or 'global finprint'
GROUP BY
  aff.name,
  u.first_name,
  u.last_name
ORDER BY
  count(a.id) desc,
  aff.name;
