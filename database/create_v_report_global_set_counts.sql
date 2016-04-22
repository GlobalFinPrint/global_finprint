-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_global_set_counts AS
  -- todo:  add an "order by", if desrired?
  SELECT
    r.name               AS region_name,
    count(DISTINCT t.id) AS trip_count,
    count(DISTINCT s.id) AS set_count
  FROM habitat_region r
    INNER JOIN habitat_location l ON l.region_id = r.id
    LEFT JOIN trip_trip t ON t.location_id = l.id
    LEFT JOIN bruv_set s ON s.trip_id = t.id
  GROUP BY
    r.name
  UNION ALL
  SELECT
    'Total'              AS region_name,
    count(DISTINCT t.id) AS trip_count,
    count(DISTINCT s.id) AS set_count
  FROM habitat_region r
    INNER JOIN habitat_location l ON l.region_id = r.id
    LEFT JOIN trip_trip t ON t.location_id = l.id
    LEFT JOIN bruv_set s ON s.trip_id = t.id;
