-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_sets_without_video AS
  WITH video_count AS (
      SELECT
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
    code,
    set_creation_date
  FROM video_count
  WHERE video_count = 0;
