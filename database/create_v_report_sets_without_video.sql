-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_sets_without_video AS
WITH video_count AS (
    SELECT
      bs.id,
      bs.reef_habitat_id,
      tt.code || '_' || bs.code AS code,
      bs.create_datetime        AS set_creation_date,
      count(avf.*)              AS video_count
    FROM bruv_set bs
      JOIN trip_trip tt ON (bs.trip_id = tt.id)
      JOIN trip_source ts ON (tt.source_id = ts.id)
      JOIN annotation_video av ON (bs.video_id = av.id)
      LEFT JOIN annotation_videofile avf ON (av.id = avf.video_id)
    WHERE
      ts.legacy = FALSE
    GROUP BY ts.id, tt.id, bs.id, av.id
)
SELECT
  rg.name              AS region_name,
  l.name               AS location_name,
  coalesce(s.name, '') AS site_name,
  coalesce(r.name, '') AS reef_name,
  vc.code,
  set_creation_date
FROM habitat_region rg
  JOIN habitat_location l ON l.region_id = rg.id
  JOIN habitat_site s ON s.location_id = l.id
  JOIN habitat_reef r ON r.site_id = s.id
  JOIN habitat_reefhabitat rh ON rh.reef_id = r.id
  JOIN video_count vc ON vc.reef_habitat_id = rh.id
WHERE video_count = 0;
