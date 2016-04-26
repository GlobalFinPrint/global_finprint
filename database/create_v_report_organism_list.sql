-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE VIEW public.v_report_organism_list AS
  SELECT
    a.id,
    a.common_name,
    a.family,
    a.genus,
    a.species,
    COALESCE(a.fishbase_key, 0)    AS fishbase_key,
    COALESCE(a.sealifebase_key, 0) AS sealifebase_key,
    ag.name as group_name
  FROM (annotation_animal a
    JOIN annotation_animalgroup ag ON ((ag.id = a.group_id)))
  ORDER BY ag.name, a.family, a.genus, a.species;
