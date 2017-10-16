CREATE VIEW public.v_report_zero_time_images AS
SELECT
  max('https://s3-us-west-2.amazonaws.com/finprint-annotator-screen-captures/prod/' ||
      tt.code || '/' || bs.code || '/' || ao.id ||
      '_' || ae.id || '.png') AS image_url,
  hab.region_name,
  hab.location_name,
  hab.site_name,
  hab.reef_name,
  hab.reef_habitat_name,
  bs.latitude,
  bs.longitude,
  bs.depth,
  bs.visibility,
  bs.trip_id,
  bs.id                       AS set_id,
  tt.code || '_' || bs.code   AS set_code
FROM annotation_event_attribute ea
  JOIN annotation_event ae ON ae.id = ea.event_id
  JOIN annotation_observation ao ON (ao.id = ae.observation_id)
  JOIN annotation_assignment aas ON (aas.id = ao.assignment_id)
  JOIN annotation_video av ON (av.id = aas.video_id)
  JOIN bruv_set bs ON (av.id = bs.video_id)
  JOIN trip_trip tt ON (tt.id = bs.trip_id)
  JOIN habitat_summary hab ON hab.reef_habitat_id = bs.reef_habitat_id
WHERE --aas.status_id > 2
  --and
  ea.attribute_id = 16
  AND ae.extent IS NOT NULL
GROUP BY
  hab.region_name,
  hab.location_name,
  hab.site_name,
  hab.reef_name,
  hab.reef_habitat_name,
  bs.latitude,
  bs.longitude,
  bs.depth,
  bs.visibility,
  bs.trip_id,
  bs.id,
  tt.code || '_' || bs.code
ORDER BY
  hab.region_name,
  hab.location_name,
  hab.site_name,
  hab.reef_name,
  hab.reef_habitat_name,
  bs.id;
