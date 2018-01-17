CREATE VIEW public.v_report_zero_time_master_images AS
SELECT
  'https://s3-us-west-2.amazonaws.com/finprint-annotator-screen-captures/prod/' ||
  tt.code || '/' || bs.code || '/' || ao.id ||
  '_' || ae.id || '.png'    AS image_url,

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
  tt.code || '_' || bs.code AS set_code,

  bs.trip_id,
  bs.id                     AS set_id

FROM annotation_masterevent me
  JOIN annotation_masterobservation mo ON (mo.id = me.master_observation_id)
  JOIN annotation_masterrecord mr ON mr.id = mo.master_record_id
  JOIN annotation_masterevent_attribute meat ON meat.masterevent_id = me.id

  -- grab the image from the source assignment ...
  JOIN annotation_observation ao ON ao.id = mo.original_id
  JOIN annotation_event ae ON ae.observation_id = ao.id
  JOIN annotation_event_attribute eat ON eat.event_id = ae.id

  JOIN bruv_set bs ON (bs.id = mr.set_id)
  JOIN trip_trip tt ON (tt.id = bs.trip_id)

  JOIN habitat_summary hab ON hab.reef_habitat_id = bs.reef_habitat_id
WHERE mr.status_id = 2 -- "complete"
      AND mo.type = 'I' -- "of interest events", not "animal events"
      AND meat.attribute_id = 16 -- zero time
ORDER BY set_code;

