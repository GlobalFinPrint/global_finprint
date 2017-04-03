CREATE or replace VIEW public.v_report_core_set_data AS

  SELECT
    tm.sampler_collaborator  AS team,
    rg.name                  AS region,
    l.name                   AS location_name,

    t.code                   AS trip_code,
    s.code                   AS set_code,

    s.set_date,

    st_asewkt(s.coordinates) AS wkt_coordinates,
    st_y(s.coordinates)      AS latitude,
    st_x(s.coordinates)      AS longitude,

    s.depth,

    s.drop_time,
    s.haul_time,
    st.name                  AS site,
    r.name                   AS reef,
    rt.type                  AS habitat,

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
    s.splendor_image_url
  FROM
    core_team tm
    INNER JOIN trip_trip t ON t.team_id = tm.id
    INNER JOIN habitat_location l ON l.id = t.location_id
    INNER JOIN habitat_region rg ON rg.id = l.region_id
    INNER JOIN bruv_set s ON s.trip_id = t.id

    INNER JOIN habitat_reefhabitat rh ON rh.id = s.reef_habitat_id
    INNER JOIN habitat_reef r ON r.id = rh.reef_id
    INNER JOIN habitat_site st ON st.id = r.site_id
    INNER JOIN habitat_reeftype rt ON rt.id = rh.habitat_id

    INNER JOIN bruv_equipment eq ON eq.id = s.equipment_id
    INNER JOIN bruv_frametype eqf ON eqf.id = eq.frame_type_id
    INNER JOIN bruv_bait bait ON bait.id = s.bait_id

    LEFT JOIN habitat_substrate sub ON sub.id = s.substrate_id
    LEFT JOIN habitat_substratecomplexity subc ON subc.id = s.substrate_complexity_id

    LEFT JOIN annotation_video v ON v.id = s.video_id
    LEFT JOIN annotation_videofile vf ON (vf.video_id = v.id AND vf."primary" = TRUE)

  ORDER BY t.code || '_' || s.code;
