/* Summary of reef level metadata */

CREATE OR REPLACE VIEW public.v_report_mpa_fishing_metadata AS
 WITH     habitat_summary AS (
        SELECT DISTINCT
          habitat_region.name                         AS region_name,
          habitat_location.name                       AS location_name,
          habitat_site.name                           AS site_name,
          habitat_site.type                           AS site_type,
          habitat_reef.name                           AS reef_name,
          habitat_region.id                       AS region_id,
          habitat_location.id                     AS location_id,
          habitat_site.id                         AS site_id,
          habitat_reef.id                         AS reef_id
        FROM habitat_region
          LEFT JOIN habitat_location ON habitat_region.id=habitat_location.region_id
          LEFT JOIN habitat_site ON habitat_location.id=habitat_site.location_id
          LEFT JOIN habitat_reef ON habitat_site.id=habitat_reef.site_id
      WHERE habitat_reef.id IS NOT NULL
    ),


 reef_metadata AS (
  /* this script makes a summary table showing all reef-level metadata, e.g. levels of fishing and compliance with MPAs */
    SELECT
      habitat_reef.id                                    AS reef_id,
      /* reef_ID acts as primary key for this table*/
      habitat_protectionstatus.type                      AS protection_status,
      habitat_mpa.name                                   AS MPA_name,
      habitat_mpa.area                                   AS MPA_area,
      habitat_mpa.founded                                AS MPA_year_founded,
      habitat_mpaisolation.type                          AS MPA_isolation,
      habitat_mpacompliance.type                         AS MPA_compliance,

      string_agg(habitat_fishingrestrictions.type,
                 ', ')                                   AS fishing_restrictions /* each reef can have multiple types of fishing restrictions */
    FROM habitat_reef
      LEFT JOIN habitat_protectionstatus ON habitat_reef.protection_status_id = habitat_protectionstatus.id
      LEFT JOIN habitat_mpa ON habitat_reef.mpa_id = habitat_mpa.id
      LEFT JOIN habitat_mpaisolation ON habitat_mpa.mpa_isolation_id = habitat_mpaisolation.id
      LEFT JOIN habitat_mpacompliance ON habitat_mpa.mpa_compliance_id = habitat_mpacompliance.id
      LEFT JOIN habitat_reef_fishing_restrictions ON habitat_reef.id = habitat_reef_fishing_restrictions.reef_id
      LEFT JOIN habitat_fishingrestrictions
        ON habitat_reef_fishing_restrictions.fishingrestrictions_id = habitat_fishingrestrictions.id
    GROUP BY
      habitat_reef.id,
      habitat_reef.name,
      habitat_protectionstatus.type,
      habitat_mpa.name,
      habitat_mpa.area,
      habitat_mpa.founded,
      habitat_mpaisolation.type,
      habitat_mpacompliance.type
),

    fishing_metadata AS (
      SELECT
        habitat_reef.id                               AS reef_id,
        string_agg(habitat_sharkgearinuse.type, '; ') AS shark_fishing_gear /* each reef can have multiple fishing gears */
      FROM habitat_reef
        LEFT JOIN habitat_reef_shark_gear_in_use ON habitat_reef.id = habitat_reef_shark_gear_in_use.reef_id
        LEFT JOIN habitat_sharkgearinuse ON habitat_reef_shark_gear_in_use.sharkgearinuse_id = habitat_sharkgearinuse.id
      GROUP BY habitat_reef.id
  )


SELECT DISTINCT
region_name,
location_name,
site_name,
site_type,
reef_name,
protection_status,
reef_metadata.mpa_name,
  mpa_area,
  mpa_year_founded,
 reef_metadata.mpa_isolation,
 reef_metadata.mpa_compliance,
  fishing_restrictions,
  shark_fishing_gear,
region_id,
location_id,
habitat_summary.site_id,
habitat_reef.id AS reef_id
  FROM habitat_reef
       LEFT JOIN habitat_summary ON habitat_reef.id=habitat_summary.reef_id
    LEFT JOIN reef_metadata ON reef_metadata.reef_id=habitat_summary.reef_id
    LEFT JOIN fishing_metadata ON fishing_metadata.reef_id=habitat_summary.reef_id
 ;
