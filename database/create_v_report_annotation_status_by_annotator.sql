-- noinspection SqlNoDataSourceInspectionForFile
CREATE VIEW v_report_annotation_status_by_annotator AS
  SELECT
    aff.name AS affiliation,
    u.first_name,
    u.last_name,
    ans.name AS status,
    count(s.video_id)
  FROM trip_trip t
    INNER JOIN bruv_set s ON s.trip_id = t.id
    INNER JOIN annotation_assignment a ON a.video_id = s.video_id
    INNER JOIN annotation_annotationstate ans ON ans.id = a.status_id
    INNER JOIN core_finprintuser an ON an.id = a.annotator_id
    INNER JOIN auth_user u ON u.id = an.user_id
    INNER JOIN core_affiliation aff ON aff.id = an.affiliation_id
  GROUP BY
    aff.name,
    u.first_name,
    u.last_name,
    ans.name
  ORDER BY
    aff.name,
    u.last_name,
    u.first_name;

