CREATE VIEW public.v_report_zero_time_assignment_images AS
SELECT
  'https://s3-us-west-2.amazonaws.com/finprint-annotator-screen-captures/prod/' ||
  tt.code || '/' || bs.code || '/' || ao.id ||
  '_' || ae.id || '.png' AS image_url,

  hab.region_name,
  hab.location_name,
  hab.site_name,
  hab.reef_name,
  hab.reef_habitat_name,

  bs.latitude,
  bs.longitude,
  bs.depth,
  bs.visibility,

  bs.set_date,
  bs.drop_time,
  tt.code || '_' || bs.code as set_code,

  bs.trip_id,
  bs.id                  AS set_id

FROM annotation_event ae
  JOIN annotation_observation ao ON (ao.id = ae.observation_id)
  JOIN annotation_assignment aas ON (aas.id = ao.assignment_id)
  JOIN annotation_video av ON (av.id = aas.video_id)
  join annotation_event_attribute eat on eat.event_id = ae.id

  JOIN bruv_set bs ON (av.id = bs.video_id)
  JOIN trip_trip tt ON (tt.id = bs.trip_id)

  JOIN habitat_summary hab on hab.reef_habitat_id = bs.reef_habitat_id

WHERE aas.status_id in (2, 3) -- "ready for review" and "reviewed" assignments
      AND ao.type = 'I' -- "of interest events", not "animal events"
      AND eat.attribute_id = 16 -- zero time

ORDER BY set_code;

