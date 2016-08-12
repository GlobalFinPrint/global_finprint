-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_sets_without_video AS
  SELECT
    tt.code || '_' || bs.code AS code,
    bs.create_datetime        AS set_creation_date
  FROM bruv_set bs
    JOIN trip_trip tt ON (bs.trip_id = tt.id)
    JOIN annotation_video av ON (bs.video_id = av.id)
    JOIN trip_source ts ON (tt.source_id = ts.id)
  WHERE
    ts.legacy = FALSE AND
    av.file IS NULL OR av.file = '';
