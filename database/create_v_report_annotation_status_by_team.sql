-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_annotation_status_by_team AS  SELECT aff.name AS affiliation,
    ans.name AS status,
    count(s.video_id) AS count
   FROM ((((((trip_trip t
     JOIN bruv_set s ON ((s.trip_id = t.id)))
     JOIN annotation_assignment a ON ((a.video_id = s.video_id)))
     JOIN annotation_annotationstate ans ON ((ans.id = a.status_id)))
     JOIN core_finprintuser an ON ((an.id = a.annotator_id)))
     JOIN auth_user u ON ((u.id = an.user_id)))
     JOIN core_affiliation aff ON ((aff.id = an.affiliation_id)))
  GROUP BY aff.name, ans.name
  ORDER BY aff.name;
