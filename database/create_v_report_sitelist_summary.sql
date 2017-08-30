-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_sitelist_summary AS
SELECT
  rg.name           AS region_name,
  l.name            AS location_name,
  s.name            AS site_name,
  r.name            AS reef_name,
  s.type            AS site_type,
  ps.type           AS protection_status,
  mpa.name          AS mpa_name,
  mpa.founded       AS mpa_founded,
  mpa.area          AS mpa_area,
  mpac.type         AS mpa_compliance_type,
  mpai.type         AS mpa_isolation,
  l.id              AS location_id,
  COALESCE(s.id, 0) AS site_id,
  r.id              AS reef_id,
  mpa.id            AS mpa_id
FROM habitat_region rg
  JOIN habitat_location l ON l.region_id = rg.id
  LEFT JOIN habitat_site s ON s.location_id = l.id
  LEFT JOIN habitat_reef r ON r.site_id = s.id
  LEFT JOIN habitat_protectionstatus ps ON ps.id = r.protection_status_id
  LEFT JOIN habitat_mpa mpa ON mpa.id = r.mpa_id
  LEFT JOIN habitat_mpacompliance mpac ON mpac.id = mpa.mpa_compliance_id
  LEFT JOIN habitat_mpaisolation mpai ON mpai.id = mpa.mpa_isolation_id
ORDER BY
  rg.name,
  l.name,
  s.name,
  r.name;
