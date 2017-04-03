CREATE or replace VIEW public.v_report_set_environmental_data AS
  WITH environmentmeasures AS
  (
    SELECT
      tm.sampler_collaborator AS team,
      rg.name                 AS region,
      l.name                  AS location_name,

      t.code                  AS trip_code,
      s.code                  AS set_code,

      s.set_date,

      'drop'                  AS drop_haul,

      dem.salinity,
      dem.conductivity,
      dem.dissolved_oxygen,
      dem.tide_state,
      dem.estimated_wind_speed,
      dem.measured_wind_speed,
      dem.wind_direction,
      dem.cloud_cover,
      dem.surface_chop

    FROM
      core_team tm
      INNER JOIN trip_trip t ON t.team_id = tm.id
      INNER JOIN habitat_location l ON l.id = t.location_id
      INNER JOIN habitat_region rg ON rg.id = l.region_id
      INNER JOIN bruv_set s ON s.trip_id = t.id

      LEFT JOIN bruv_environmentmeasure dem ON dem.id = s.drop_measure_id
    UNION
    SELECT
      tm.sampler_collaborator AS team,
      rg.name                 AS region,
      l.name                  AS location_name,

      t.code                  AS trip_code,
      s.code                  AS set_code,

      s.set_date,

      'haul'                  AS drop_haul,

      hem.salinity,
      hem.conductivity,
      hem.dissolved_oxygen,
      hem.tide_state,
      hem.estimated_wind_speed,
      hem.measured_wind_speed,
      hem.wind_direction,
      hem.cloud_cover,
      hem.surface_chop

    FROM
      core_team tm
      INNER JOIN trip_trip t ON t.team_id = tm.id
      INNER JOIN habitat_location l ON l.id = t.location_id
      INNER JOIN habitat_region rg ON rg.id = l.region_id
      INNER JOIN bruv_set s ON s.trip_id = t.id

      LEFT JOIN bruv_environmentmeasure hem ON hem.id = s.haul_measure_id
  )
  SELECT
    em.team,
    em.region,
    em.location_name,
    em.trip_code,
    em.set_code,
    em.set_date,
    em.drop_haul,

    em.salinity,
    em.conductivity,
    em.dissolved_oxygen,
    em.tide_state,
    em.estimated_wind_speed,
    em.measured_wind_speed,
    em.wind_direction,
    em.cloud_cover,
    em.surface_chop
  FROM environmentmeasures em
  ORDER BY em.trip_code || '_' || em.set_code,
    em.drop_haul;

