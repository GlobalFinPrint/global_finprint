-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_set_counts_by_location AS
  SELECT
    r.name               AS region_name,
    l.name               AS location_name,
    count(DISTINCT t.id) AS trip_count,
    count(DISTINCT s.id) AS set_count
  FROM habitat_region r
    INNER JOIN habitat_location l ON l.region_id = r.id
    LEFT JOIN trip_trip t ON t.location_id = l.id
    LEFT JOIN bruv_set s ON s.trip_id = t.id
  GROUP BY
    r.name,
    l.name
  ORDER BY
    r.name,
    l.name;
