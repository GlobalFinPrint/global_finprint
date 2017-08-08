CREATE OR REPLACE FUNCTION public.text_time(integer_time integer) RETURNS text AS $$
        BEGIN
          RETURN ((((lpad(((((integer_time) / 1000) / 60))::text, 3, '0'::text) || ':'::text)
            || lpad(((((integer_time) / 1000) % 60))::text, 2, '0'::text)) || ':'::text)
            || lpad((((integer_time) % 1000))::text, 3, '0'::text));
        END;
$$ LANGUAGE plpgsql;
