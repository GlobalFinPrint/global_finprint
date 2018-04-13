CREATE VIEW public.v_report_machine_learning_corpus_from_assignment AS
SELECT
  'https://s3-us-west-2.amazonaws.com/finprint-annotator-screen-captures/prod/' ||
  tt.code || '/' || bs.code || '/' || ao.id ||
  '_' || ae.id || '.png' AS image_url,
  ST_AsText(ae.extent)   AS bounding_box,
  aag.name               AS animal_group,
  aa.family              AS animal_family,
  aa.genus               AS animal_genus,
  aa.species             AS animal_species,
  hr.name                AS region,
  lo.name                AS location_name,
  st.name                AS site_name,
  rf.name                AS reef_name,
  rt.type                AS reef_habitat,
  bs.latitude,
  bs.longitude,
  bs.depth,
  bs.visibility,
  ae.event_time,
  av.id                  AS video_id,
  ao.id                  AS observation_id,
  ae.id                  AS event_id
FROM annotation_event ae
  JOIN annotation_observation ao ON (ao.id = ae.observation_id)
  JOIN annotation_assignment aas ON (aas.id = ao.assignment_id)
  JOIN annotation_video av ON (av.id = aas.video_id)
  JOIN bruv_set bs ON (av.id = bs.video_id)
  JOIN trip_trip tt ON (tt.id = bs.trip_id)
  JOIN annotation_animalobservation aao ON (ao.id = aao.observation_id)
  JOIN annotation_animal aa ON (aa.id = aao.animal_id)
  JOIN annotation_animalgroup aag ON (aag.id = aa.group_id)
  JOIN annotation_animal_regions aar ON (aa.id = aar.animal_id)
  JOIN habitat_region hr ON (hr.id = aar.region_id)
  JOIN habitat_reefhabitat rh ON rh.id = bs.reef_habitat_id
  JOIN habitat_reeftype rt ON rt.id = rh.habitat_id
  JOIN habitat_reef rf ON rf.id = rh.reef_id
  JOIN habitat_site st ON st.id = rf.site_id
  JOIN habitat_location lo ON lo.id = st.location_id
WHERE aas.status_id > 2
      AND ao.type = 'A'
      AND ae.extent IS NOT NULL
ORDER BY region,
  animal_group,
  animal_family,
  animal_genus,
  animal_species;
