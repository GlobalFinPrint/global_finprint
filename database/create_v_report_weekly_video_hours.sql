CREATE VIEW public.v_report_weekly_video_hours AS
  WITH datum_seq AS
  (
      SELECT '2016-01-01' :: DATE + SEQUENCE.DAY AS datum
      FROM generate_series(0, 1000) AS SEQUENCE(DAY)
      GROUP BY SEQUENCE.DAY
      ORDER BY datum
  ),
      weekly_totals AS
    (
        SELECT
          to_char(d.datum, 'iyyy/IW')                                                      AS year_week,
          coalesce(sum(a.progress_delta) :: NUMERIC / 1000 / 60 / 60, 0) :: NUMERIC(16, 2) AS weekly_progress
        FROM annotation_activity_audit a
          RIGHT JOIN datum_seq d ON d.datum = a.activity_datetime :: DATE
        WHERE d.datum <= (SELECT max(activity_datetime :: DATE)
                          FROM annotation_activity_audit)
              AND d.datum >= (SELECT min(activity_datetime :: DATE)
                              FROM annotation_activity_audit)
        GROUP BY year_week
        ORDER BY year_week DESC
    )
  SELECT
    year_week,
    weekly_progress,
    sum(weekly_progress)
    OVER (
      ORDER BY year_week) AS running_sum
  FROM weekly_totals
  ORDER BY year_week;
