
-- report views
DROP VIEW IF EXISTS public.v_report_annotation_status_by_annotator;
DROP VIEW IF EXISTS public.v_report_annotation_status_by_team;

Drop VIEW if exists public.v_report_assignment_status_by_file;
Drop VIEW if exists public.v_report_assignment_status;

DROP VIEW IF EXISTS public.set_summary;
Drop VIEW if exists public.v_report_core_set_data;
Drop VIEW if exists public.v_report_set_environmental_data;

DROP VIEW IF EXISTS public.v_report_global_set_counts;
DROP VIEW IF EXISTS public.v_report_global_set_counts_by_source;

DROP VIEW IF EXISTS public.v_report_organism_list;

DROP VIEW IF EXISTS public.v_report_set_counts_by_location;

DROP VIEW IF EXISTS public.v_report_sets_without_video;

DROP VIEW IF EXISTS public.v_report_sitelist_summary;

DROP VIEW IF EXISTS public.v_report_species_observation_counts;

DROP VIEW IF EXISTS public.v_report_usage_metrics;
DROP VIEW IF EXISTS public.v_report_usage_metrics_by_affiliation;

DROP VIEW IF EXISTS public.v_report_weekly_video_hours;

-- observation summaries:
DROP VIEW IF EXISTS public.v_report_observations_wa;
DROP VIEW IF EXISTS public.v_report_observations_io;
DROP VIEW IF EXISTS public.v_report_observations_pac;
DROP VIEW IF EXISTS public.v_report_observations_coral;

DROP VIEW IF EXISTS public.v_report_observations_wa_summary;
DROP VIEW IF EXISTS public.v_report_observations_io_summary;
DROP VIEW IF EXISTS public.v_report_observations_pac_summary;
DROP VIEW IF EXISTS public.v_report_observations_coral_summary;

DROP VIEW IF EXISTS public.v_report_observations_master;

DROP VIEW IF EXISTS public.legacy_observation_summary;
DROP VIEW IF EXISTS public.observation_summary;

DROP VIEW IF EXISTS public.v_report_maxn_observations;
DROP VIEW IF EXISTS public.v_report_maxn_elasmobranch_observations;

-- reef completion:
DROP VIEW IF EXISTS public.v_report_reef_summary;
DROP VIEW IF EXISTS public.v_report_reef_annotations_summary;
DROP VIEW IF EXISTS public.v_report_fishing_mpa_metadata;

-- data QC:
DROP VIEW IF EXISTS public.v_report_maxn_issues_report;

-- other useful stuff:
DROP VIEW IF EXISTS public.v_report_machine_learning_corpus;

-- supporting views
DROP VIEW IF EXISTS public.event_attribute_summary;
DROP VIEW IF EXISTS public.master_attribute_summary;
DROP VIEW IF EXISTS public.habitat_summary;
DROP VIEW IF EXISTS public.overall_leaderboard;
DROP VIEW IF EXISTS public.monthly_leaderboard;
