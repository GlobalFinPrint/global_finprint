CREATE OR REPLACE VIEW public.v_report_observations_io_summary AS
select
  summary_id,
  trip_code,
  set_code,
  full_code,

  region_name,
  location_name,
  site_name,
  reef_name,
  reef_habitat_name,

  animal_id,
  family,
  genus,
  species,

  maxn,
  event_time_minutes_raw,
  event_time_minutes,

  trip_id,
  set_id,
  video_id
from public.observation_summary
where
  lower(region_name) = lower('indian ocean')
order by
  location_name,
  full_code,
  event_time_minutes;
