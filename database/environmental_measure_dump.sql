WITH environmental_measures AS
(
  SELECT
    t.code                AS trip_code,
    bs.code               AS set_code,
    bs.set_date           AS "date",
    'drop'                AS drop_haul,
    dem.water_temperature AS temp,
    dem.salinity,
    dem.conductivity,
    dem.dissolved_oxygen,
    dem.current_flow,
    dem.current_direction,
    dem.tide_state,
    dem.estimated_wind_speed,
    dem.measured_wind_speed,
    dem.wind_direction,
    dem.cloud_cover,
    dem.surface_chop

  FROM bruv_set bs
    INNER JOIN trip_trip t ON t.id = bs.trip_id
    INNER JOIN bruv_environmentmeasure dem ON dem.id = bs.drop_measure_id
--   WHERE t.code IN
--         (
--           -- sample dump for Gina:
--           'FP_2016_BS_02',
--           'FP_2016_BS_03',
--           'FP_2016_BS_04'
--         )
  UNION
  SELECT
    t.code                AS trip_code,
    bs.code               AS set_code,
    bs.set_date           AS "date",
    'haul'                AS drop_haul,
    dem.water_temperature AS temp,
    dem.salinity,
    dem.conductivity,
    dem.dissolved_oxygen,
    dem.current_flow,
    dem.current_direction,
    dem.tide_state,
    dem.estimated_wind_speed,
    dem.measured_wind_speed,
    dem.wind_direction,
    dem.cloud_cover,
    dem.surface_chop

  FROM bruv_set bs
    INNER JOIN trip_trip t ON t.id = bs.trip_id
    INNER JOIN bruv_environmentmeasure dem ON dem.id = bs.haul_measure_id
--   WHERE t.code IN
--         (
--           -- sample dump for Gina:
--           'FP_2016_BS_02',
--           'FP_2016_BS_03',
--           'FP_2016_BS_04'
--         )
)
SELECT
  trip_code,
  set_code,
  "date",
  drop_haul,
  temp,
  salinity,
  conductivity,
  dissolved_oxygen,
  current_flow,
  current_direction,
  tide_state,
  estimated_wind_speed,
  measured_wind_speed,
  wind_direction,
  cloud_cover,
  surface_chop
FROM environmental_measures
ORDER BY trip_code,
  set_code,
  drop_haul;
