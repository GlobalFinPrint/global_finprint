-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_sitelist_summary AS
SELECT
  rg.name                  AS region_name,
  l.name                   AS location_name,
  coalesce(s.name, '')     AS site_name,
  coalesce(r.name, '')     AS reef_name,

  coalesce(s.type, '')     AS site_type,
  coalesce(ps.type, '')    AS protection_status,
  coalesce(mpa.name, '')   AS mpa_name,
  coalesce(mpa.founded, 0) AS mpa_founded,
  coalesce(mpa.area, 0.0)  AS mpa_area,
  coalesce(mpac.type, '')  AS mpa_compliance_type,
  coalesce(mpai.type, '')  AS mpa_isolation,

  l.code                   AS location_code,
  coalesce(s.code, '')     AS site_code,
  coalesce(r.code, '')     AS region_code,

  l.id                     AS location_id,
  COALESCE(s.id, 0)        AS site_id,
  coalesce(r.id, 0)        AS reef_id,
  coalesce(mpa.id, 0)      AS mpa_id
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
