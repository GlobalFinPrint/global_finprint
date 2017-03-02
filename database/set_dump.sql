SELECT
  t.code                        AS trip_code,
  bs.code                       AS set_code,
  bs.set_date                   AS "date",
  bs.latitude,
  bs.longitude,

  bs.depth,
  bs.drop_time,
  bs.haul_time,

  st.name                       AS site,
  rf.name                       AS reef,
  h.type                        AS habitat,

  ft.type || ' / ' || eq.camera AS equipment,

  CASE
  WHEN bt.type = 'CRS'
    THEN 'Crushed '
  WHEN bt.type = 'CHP'
    THEN 'Chopped '
  WHEN bt.type = 'WHL'
    THEN 'Whole '
  ELSE ''
  END || bt.description         AS bait,

  bs.visibility,

  vf.file                       AS video_file_name,
  vf.source                     AS video_source,
  vf.path                       AS video_path,

  bs.comments                   AS comment

FROM bruv_set bs
  INNER JOIN trip_trip t ON t.id = bs.trip_id

  INNER JOIN bruv_equipment eq ON eq.id = bs.equipment_id
  INNER JOIN bruv_frametype ft ON ft.id = eq.frame_type_id
  INNER JOIN bruv_bait bt ON bt.id = bs.bait_id

  INNER JOIN habitat_reefhabitat rh ON rh.id = bs.reef_habitat_id
  INNER JOIN habitat_reeftype h ON h.id = rh.habitat_id
  INNER JOIN habitat_reef rf ON rf.id = rh.reef_id
  INNER JOIN habitat_site st ON st.id = rf.site_id
  INNER JOIN habitat_location lo ON lo.id = st.location_id

  LEFT JOIN annotation_video v ON v.id = bs.video_id
  LEFT JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)

-- -- this should be limited or it is rather large ...
-- where t.code in
-- (
--   -- dump for Gina:
--   'FP_2016_BS_02',
--   'FP_2016_BS_03',
--   'FP_2016_BS_04'
-- )
ORDER BY
  t.code,
  bs.code;
