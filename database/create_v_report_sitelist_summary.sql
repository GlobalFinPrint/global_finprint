-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_sitelist_summary AS
  SELECT
    r.id              AS reef_id,
    l.id              AS location_id,
    COALESCE(s.id, 0) AS site_id,
    rg.name           AS region_name,
    ((((('FP_xxxx_' :: TEXT || (l.code) :: TEXT) || '_xx_' :: TEXT) ||
       (COALESCE(s.code, '' :: CHARACTER VARYING)) :: TEXT) || (COALESCE(r.code, '' :: CHARACTER VARYING)) :: TEXT) ||
     '_xx' :: TEXT)   AS code_aggragation,
    COALESCE(
        ((((l.name) :: TEXT || ' (' :: TEXT) || (COALESCE(l.code, '' :: CHARACTER VARYING)) :: TEXT) || ')' :: TEXT),
        '' :: TEXT)   AS location,
    COALESCE(
        ((((s.name) :: TEXT || ' (' :: TEXT) || (COALESCE(s.code, '' :: CHARACTER VARYING)) :: TEXT) || ')' :: TEXT),
        '' :: TEXT)   AS site,
    COALESCE(
        ((((r.name) :: TEXT || ' (' :: TEXT) || (COALESCE(r.code, '' :: CHARACTER VARYING)) :: TEXT) || ')' :: TEXT),
        '' :: TEXT)   AS reef,
    '' :: TEXT        AS investigator,
    '' :: TEXT        AS partner,
    s.type,
    ps.type           AS protection_status
  FROM ((((habitat_region rg
                          JOIN habitat_location l ON ((l.region_id = rg.id)))
           LEFT JOIN habitat_site s ON ((s.location_id = l.id)))
          LEFT JOIN habitat_reef r ON ((r.site_id = s.id)))
    LEFT JOIN habitat_protectionstatus ps ON ((ps.id = r.protection_status_id)))
  ORDER BY rg.name, l.name, s.name, r.name;
