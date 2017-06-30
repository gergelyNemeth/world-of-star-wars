ALTER TABLE IF EXISTS ONLY public.user DROP CONSTRAINT IF EXISTS pk_sw_user_id CASCADE;

DROP TABLE IF EXISTS public.user;
DROP SEQUENCE IF EXISTS public.user_id_seq;
CREATE TABLE public.user (
    id serial NOT NULL,
    username VARCHAR UNIQUE,
    password VARCHAR
    );

ALTER TABLE ONLY public.user
    ADD CONSTRAINT pk_sw_user_id PRIMARY KEY (id);
