-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_global_set_counts_by_source AS  SELECT r.name AS region_name,
    sr.name AS source,
    count(DISTINCT t.id) AS trip_count,
    count(DISTINCT s.id) AS set_count
   FROM ((((habitat_region r
     JOIN habitat_location l ON ((l.region_id = r.id)))
     JOIN trip_trip t ON ((t.location_id = l.id)))
     JOIN trip_source sr ON ((sr.id = t.source_id)))
     left JOIN bruv_set s ON ((s.trip_id = t.id)))
  GROUP BY sr.name, r.name
UNION ALL
 SELECT 'Total'::character varying AS region_name,
    '' AS source,
    count(DISTINCT t.id) AS trip_count,
    count(DISTINCT s.id) AS set_count
   FROM ((((habitat_region r
     JOIN habitat_location l ON ((l.region_id = r.id)))
     JOIN trip_trip t ON ((t.location_id = l.id)))
     JOIN trip_source sr ON ((sr.id = t.source_id)))
     left JOIN bruv_set s ON ((s.trip_id = t.id)));
