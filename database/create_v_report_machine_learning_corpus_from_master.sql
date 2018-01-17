CREATE VIEW public.v_report_machine_learning_corpus_from_master AS
SELECT
  'https://s3-us-west-2.amazonaws.com/finprint-annotator-screen-captures/prod/' ||
  tt.code || '/' || bs.code || '/' || ao.id ||
  '_' || ae.id || '.png' AS image_url,
  ST_AsText(ae.extent)   AS bounding_box,
  aag.name               AS animal_group,
  aa.family              AS animal_family,
  aa.genus               AS animal_genus,
  aa.species             AS animal_species,
  hs.region_name,
  hs.location_name,
  hs.site_name,
  hs.reef_name,
  hs.reef_habitat_name,
  bs.latitude,
  bs.longitude,
  bs.depth,
  bs.visibility,
  ae.event_time,
  ao.id                  AS observation_id,
  ae.id                  AS event_id,
  bs.bulk_loaded,
  bs.comments
FROM annotation_masterevent ae
  JOIN annotation_masterobservation ao ON (ao.id = ae.master_observation_id)
  JOIN annotation_masterrecord mr ON (mr.id = ao.master_record_id)
  JOIN bruv_set bs ON (mr.set_id = bs.id)
  JOIN trip_trip tt ON (tt.id = bs.trip_id)
  JOIN annotation_masteranimalobservation aao ON (ao.id = aao.master_observation_id)
  JOIN annotation_animal aa ON (aa.id = aao.animal_id)
  JOIN annotation_animalgroup aag ON (aag.id = aa.group_id)
  JOIN annotation_animal_regions aar ON (aa.id = aar.animal_id)
  JOIN habitat_summary hs on hs.reef_habitat_id = bs.reef_habitat_id
WHERE mr.status_id = 2
      AND ao.type = 'A'
      AND ae.extent IS NOT NULL
      --and hs.region_name = 'Western Atlantic'
ORDER BY
  tt.code,
  bs.code,
  animal_group,
  animal_family,
  animal_genus,
  animal_species;
