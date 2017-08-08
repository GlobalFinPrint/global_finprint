CREATE OR REPLACE VIEW public.set_summary AS
SELECT
  s.id as set_id,
  tm.sampler_collaborator  AS team,

  t.code                   AS trip_code,
  s.code                   AS set_code,

  hab.region_name,
  hab.location_name,
  hab.site_name,
  hab.reef_name,
  hab.reef_habitat_name,

  s.reef_habitat_id,

  s.set_date,
  s.drop_time,
  s.haul_time,

  st_asewkt(s.coordinates) AS wkt_coordinates,
  st_y(s.coordinates)      AS latitude,
  st_x(s.coordinates)      AS longitude,

  s.depth,

  eqf.type                 AS equipment_frame_type,
  eq.camera                AS equipment_camera,
  eq.stereo                AS equipment_stereo_camera,
  eq.camera_height         AS equipment_camera_height,
  eq.arm_length            AS equipment_arm_length,

  bait.type                AS bait_preparation,
  bait.description         AS bait_type,
  bait.oiled               AS bait_oiled,

  s.visibility,

  s.current_flow_estimated,
  s.current_flow_instrumented,

  sub.type                 AS substrate_type,
  subc.name                AS substrate_complexity_type,
  s.bruv_image_url,
  s.splendor_image_url,

  vf.file                  AS video_file_name,
  vf.source                AS video_source,
  vf.path                  AS video_path
FROM
  core_team tm
  INNER JOIN trip_trip t ON t.team_id = tm.id
  INNER JOIN bruv_set s ON s.trip_id = t.id

  INNER JOIN habitat_summary hab ON hab.reef_habitat_id = s.reef_habitat_id

  INNER JOIN bruv_equipment eq ON eq.id = s.equipment_id
  INNER JOIN bruv_frametype eqf ON eqf.id = eq.frame_type_id
  INNER JOIN bruv_bait bait ON bait.id = s.bait_id

  LEFT JOIN habitat_substrate sub ON sub.id = s.substrate_id
  LEFT JOIN habitat_substratecomplexity subc ON subc.id = s.substrate_complexity_id

  LEFT JOIN annotation_video v ON v.id = s.video_id
  LEFT JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)
ORDER BY t.code || '_' || s.code;
