CREATE OR REPLACE VIEW public.v_report_observations_coral_summary AS
select
  trip_code,
  set_code,
  has_complete_master,

  region_name,
  location_name,
  site_name,
  reef_name,
  reef_type,

  animal_id,
  family,
  genus,
  species,
  common_name,

  maxn,
  event_time_mil,
  event_time_mins,

  set_id,
  set_lat,
  set_long
from public.v_report_maxn_observations
where
  lower(region_name) = lower('coral triangle')
order by
  location_name,
  set_id,
  event_time_mil;
