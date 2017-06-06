CREATE VIEW public.v_report_maxn_issues_report AS
  SELECT
    CASE
    WHEN evt.max_n_tagged = 1
         AND evt.numeric_value_from_obs_comment IS NOT NULL
         AND evt.numeric_value_from_event_note IS NULL
      THEN 1
    ELSE 0
    END                                                                               AS obs_comment_may_be_maxn,

    CASE
    WHEN evt.max_n_tagged = 0
         AND evt.numeric_value_from_event_note IS NOT NULL
      THEN 1
    ELSE 0
    END                                                                               AS no_tag_evt_note_may_be_maxn,

    CASE
    WHEN evt.max_n_tagged = 1
         AND evt.numeric_value_from_obs_comment IS NULL
         AND evt.numeric_value_from_event_note IS NULL
      THEN 1
    ELSE 0
    END                                                                               AS maxn_tag_no_n,

    hab.location,
    hab.site,
    hab.reef,

    evt.trip_code,
    evt.set_code,

    u.last_name,
    u.first_name,

    evt.event_time,
    -- format event time to xx:xx:xxx
    lpad((((evt.event_time / 1000) / 60) :: TEXT), 3, '0')
    || ':' || lpad(((evt.event_time / 1000) % 60) :: TEXT, 2, '0')
    || ':' || lpad(((evt.event_time % 1000) :: TEXT), 3, '0')                         AS event_time_minutes,

    evt.assignment_id,
    'https://data.globalfinprint.org/assignment/review/' || evt.assignment_id :: TEXT AS assignment_management_url,


    evt.max_n_tagged,
    evt.numeric_value_from_event_note,
    evt.numeric_value_from_obs_comment,
    obs.comment                                                                       AS observation_comment,
    aevt.note                                                                         AS event_note,
    ani.genus,
    ani.species

  FROM event_attribute_summary evt
    INNER JOIN habitat_summary hab ON hab.reef_habitat_id = evt.reef_habitat_id
    INNER JOIN annotation_observation obs ON obs.id = evt.observation_id
    INNER JOIN annotation_event aevt ON aevt.id = evt.event_id
    INNER JOIN core_finprintuser fpuser ON fpuser.id = evt.annotator_id
    INNER JOIN auth_user u ON u.id = fpuser.user_id
    LEFT JOIN annotation_animal ani ON ani.id = evt.animal_id
  WHERE (evt.numeric_value_from_event_note IS NOT NULL
         OR evt.numeric_value_from_obs_comment IS NOT NULL
         OR evt.max_n_tagged = 1)
  -- and lower(hab.region) = 'western atlantic'
  ORDER BY
    hab.location,
    hab.site,
    hab.reef,
    evt.assignment_id,
    evt.event_time;
