-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_species_observation_counts AS
  WITH animal_observations AS
  (
      -- todo:  DRY ... pull this into another view that can be reused ... add other observation data as well.
      SELECT
        t.id   AS trip_id,
        t.location_id,
        ani.id AS animal_id,
        ani.common_name,
        ani.family,
        ani.genus,
        ani.species
      FROM trip_trip t
        INNER JOIN bruv_set s ON s.trip_id = t.id
        INNER JOIN annotation_assignment a ON a.video_id = s.video_id
        INNER JOIN annotation_observation o ON o.assignment_id = a.id
        INNER JOIN annotation_animalobservation ao ON ao.observation_id = o.id
        INNER JOIN annotation_animal ani ON ani.id = ao.animal_id
  )
  SELECT
    r.name                                                                    AS region_name,
    coalesce(o.common_name || ' (' || o.genus || ' ' || o.species || ')', '') AS animal,
    count(1)                                                                  AS animal_count
  FROM habitat_region r
    INNER JOIN habitat_location l ON l.region_id = r.id
    INNER JOIN animal_observations o ON o.location_id = l.id
  GROUP BY
    r.name,
    o.common_name,
    o.genus,
    o.species
  ORDER BY r.name,
    o.genus,
    o.species;
