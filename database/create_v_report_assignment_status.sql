CREATE OR REPLACE VIEW public.v_report_assignment_status AS
SELECT
  vf.file                                                 AS primary_video_file_name,
  vf.source                                               AS video_source,
  vf.path                                                 AS video_path,

  t.code                                                  AS trip,
  s.code                                                  AS set,

  hab.region_name,
  hab.location_name,
  hab.site_name,
  hab.reef_name,
  hab.reef_habitat_name,

  u.first_name                                            AS annotator_first_name,
  u.last_name                                             AS annotator_last_name,
  af.name                                                 AS affiliation,

  pro.name                                                AS project,

  asig.create_datetime                                    AS date_assigned,
  asig.last_modified_datetime                             AS last_progress,

  asigstat.name                                           AS status,

  asig.progress                                           AS progress,
  ((asig.progress / 1000) / 60) :: TEXT || ':'
  || lpad(((asig.progress / 1000) % 60) :: TEXT, 2, '0' :: TEXT) || ':'
  || lpad((asig.progress % 1000) :: TEXT, 3, '0' :: TEXT) AS progress_formatted

FROM
  core_team tm
  INNER JOIN trip_trip t ON t.team_id = tm.id
  INNER JOIN bruv_set s ON s.trip_id = t.id
  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = s.reef_habitat_id

  INNER JOIN annotation_video v ON v.id = s.video_id
  INNER JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)
  INNER JOIN annotation_assignment asig ON asig.video_id = v.id
  INNER JOIN core_finprintuser fp ON fp.id = asig.annotator_id
  INNER JOIN core_affiliation af ON af.id = fp.affiliation_id
  INNER JOIN auth_user u ON u.id = fp.user_id
  INNER JOIN annotation_project pro ON pro.id = asig.project_id
  INNER JOIN annotation_annotationstate asigstat ON asigstat.id = asig.status_id

ORDER BY t.code || '_' || s.code;
