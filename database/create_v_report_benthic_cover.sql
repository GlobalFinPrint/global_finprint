--- script to create standard report for finprint website,including benthic data
---  requires benthic data, set ids and codes, trip ids and codes, and site, location & region info

CREATE OR REPLACE VIEW public.v_report_benthic_cover AS
--make table with set and location information so you know which set you're looking at
WITH set_overview AS (
  SELECT
      habitat_region.name AS region_name,
  habitat_location.name AS location_name,
  habitat_site.name AS site_name,
  habitat_reef.name AS reef_name,
  habitat_reeftype.type AS reef_type,
  habitat_reef.id AS reef_id,
  trip_trip.code AS trip_code,
  extract(YEAR FROM trip_trip.start_date) :: TEXT AS trip_year,
      bruv_set.visibility,
  bruv_set.substrate_relief_mean,
  bruv_set.substrate_relief_sd,
  bruv_set.field_of_view,
  bruv_set.depth,
  bruv_set.id AS set_id,
  bruv_set.code AS set_code
FROM habitat_region
  FULL OUTER JOIN habitat_location ON habitat_region.id = habitat_location.region_id
  FULL OUTER JOIN habitat_site ON habitat_location.id = habitat_site.location_id
  FULL OUTER JOIN habitat_reef ON habitat_site.id = habitat_reef.site_id
  FULL OUTER JOIN habitat_reefhabitat ON habitat_reef.id = habitat_reefhabitat.reef_id
  FULL OUTER JOIN habitat_reeftype ON habitat_reefhabitat.habitat_id = habitat_reeftype.id
  FULL OUTER JOIN bruv_set ON habitat_reefhabitat.id = bruv_set.reef_habitat_id
  LEFT JOIN trip_trip ON bruv_set.trip_id = trip_trip.id),
--make benthic cover table with names of benthic habitat types
 benthic AS (
  SELECT
  cv.id AS benthicvalue_id,
  cv.value AS benthic_cover,
  cv.set_id,
  bc.name AS benthic_category
FROM bruv_benthiccategoryvalue cv
LEFT JOIN bruv_benthiccategory bc ON cv.benthic_category_id=bc.id),

benthic_pivot AS(
    SELECT * FROM crosstab (
      'SELECT set_id, benthic_category, benthic_cover
      FROM benthic
      ORDER BY 1,2'
    )
      AS benthic(set_id int, Ascidians int,  bleached_corals int,  Bryozoa int, Consolidated int, Crinoids int,
                  Halimeda int, hard_coral int, Hydrocoral int, Hydroids int,	invertebrate_complex int,	Macroalgae int,
                  Mangrove int, Seagrass	int, Soft_coral int,	Sponge int,
                  True_anemones	int, Unconsolidated int,	Zoanthids int))

-- put together benthic cover with set and location descriptors
SELECT
  --location descriptors
      region_name,
      location_name,
      site_name,
      reef_name,
      reef_type,
      trip_code,
      trip_year,
      set_code,
  -- envr set descriptors
     visibility,
    field_of_view,
    substrate_relief_sd,
    substrate_relief_mean,
    depth,
  -- benthic data
    Ascidians,
    bleached_corals,
    Bryozoa,
    Consolidated,
    Crinoids,
    halimeda,
    hard_coral,
    hydrocoral,
    hydroids,
    invertebrate_complex,
    macroalgae,
    mangrove,
    seagrass,
    soft_coral,
    sponge,
    True_anemones,
    unconsolidated,
    zoanthids,
-- ids
      reef_id,
      set_overview.set_id
FROM set_overview
LEFT JOIN benthic_pivot ON set_overview.set_id=benthic_pivot.set_id;
