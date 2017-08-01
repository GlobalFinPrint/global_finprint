CREATE VIEW public.habitat_summary AS
  SELECT
    hrh.id   AS reef_habitat_id,
    hrg.name AS region_name,
    hlc.name AS location_name,
    hst.name AS site_name,
    hrf.name AS reef_name,
    hrt.type AS reef_habitat_name,
    hrg.id   AS region_id,
    hlc.id   AS location_id,
    hst.id   AS site_id,
    hrf.id   AS reef_id
  FROM (((((habitat_reefhabitat hrh
    JOIN habitat_reef hrf ON ((hrf.id = hrh.reef_id)))
    JOIN habitat_site hst ON ((hst.id = hrf.site_id)))
    JOIN habitat_location hlc ON ((hlc.id = hst.location_id)))
    JOIN habitat_region hrg ON ((hrg.id = hlc.region_id)))
    JOIN habitat_reeftype hrt ON ((hrt.id = hrh.habitat_id)));

