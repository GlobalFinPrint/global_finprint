CREATE or replace VIEW public.v_report_core_set_data AS
WITH assignment_status_summary AS
(
    SELECT
      assig.video_id,
      assigst.id   AS assignment_status_id,
      assigst.name AS assignment_status,
      count(*)     AS status_count
    FROM annotation_assignment assig
      INNER JOIN annotation_annotationstate assigst ON assigst.id = assig.status_id
    GROUP BY assig.video_id,
      assigst.id,
      assigst.name
),
total_assignments as
  (
    select video_id,
      sum(status_count) as total
    from assignment_status_summary
    group by video_id
  )
SELECT
  tm.sampler_collaborator  AS team,
  hab.region_name,
  hab.location_name,

  t.code                   AS trip_code,
  s.code                   AS set_code,

  s.set_date,

  st_asewkt(s.coordinates) AS wkt_coordinates,
  st_y(s.coordinates)      AS latitude,
  st_x(s.coordinates)      AS longitude,

  s.depth,

  hab.site_name,
  hab.reef_name,
  hab.reef_habitat_name,

  s.drop_time,
  s.haul_time,

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

  vf.file                  AS video_file_name,
  vf.source                AS video_source,
  vf.path                  AS video_path,

  sub.type                 AS substrate_type,
  subc.name                AS substrate_complexity_type,
  CASE WHEN (SELECT id
             FROM bruv_benthiccategoryvalue bcv
             WHERE bcv.set_id = s.id
             LIMIT 1) IS NOT NULL
    THEN TRUE
  ELSE FALSE
  END                      AS has_bethic_categories,

  s.comments,
  s.message_to_annotators,
  s.bruv_image_url,
  s.splendor_image_url,

  coalesce(assstat.status_count, 0) as reviewed_assignments,
  coalesce(totassig.total, 0) as total_assignments,
  ms.name                  AS master_record_state

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

  LEFT JOIN annotation_masterrecord mas ON mas.set_id = s.id
  LEFT JOIN annotation_masterrecordstate ms ON ms.id = mas.status_id

  LEFT JOIN assignment_status_summary assstat ON (assstat.video_id = v.id
    and assstat.assignment_status_id = 4)
  left join total_assignments totassig on totassig.video_id = v.id
ORDER BY t.code || '_' || s.code;
