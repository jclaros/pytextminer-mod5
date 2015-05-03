CREATE TABLE public.dim_category (
                idw_category INTEGER NOT NULL,
                category VARCHAR(150) NOT NULL,
                description VARCHAR(250) NOT NULL,
                CONSTRAINT idw_category PRIMARY KEY (idw_category)
);


CREATE TABLE public.dim_weighting (
                idw_weighting INTEGER NOT NULL,
                segment VARCHAR(150) NOT NULL,
                weighting INTEGER NOT NULL,
                description VARCHAR(250) NOT NULL,
                CONSTRAINT idw_weighting PRIMARY KEY (idw_weighting)
);
COMMENT ON TABLE public.dim_weighting IS 'ponderacion';


CREATE TABLE public.dim_social_network (
                idw_social_network INTEGER NOT NULL,
                name VARCHAR(150) NOT NULL,
                description VARCHAR(250) NOT NULL,
                url VARCHAR(250) NOT NULL,
                CONSTRAINT idw_social_network PRIMARY KEY (idw_social_network)
);


CREATE TABLE public.dim_company (
                idw_company INTEGER NOT NULL,
                id BIGINT NOT NULL,
                name VARCHAR(150) NOT NULL,
                description VARCHAR(270) NOT NULL,
                link VARCHAR(250) NOT NULL,
                user_name VARCHAR(150) NOT NULL,
                CONSTRAINT idw_company PRIMARY KEY (idw_company)
);


CREATE TABLE public.dim_time (
                idw_date DATE NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                day INTEGER NOT NULL,
                month_string VARCHAR(25) NOT NULL,
                day_string VARCHAR(25) NOT NULL,
                week INTEGER NOT NULL,
                week_string VARCHAR(25) NOT NULL,
                CONSTRAINT date PRIMARY KEY (idw_date)
);


CREATE TABLE public.fact_dictionary (
                idw_date DATE NOT NULL,
                word VARCHAR(150) NOT NULL,
                description VARCHAR(250) NOT NULL,
                CONSTRAINT date1 PRIMARY KEY (idw_date)
);


CREATE TABLE public.fact_word (
                idw_date DATE NOT NULL,
                idw_weighting INTEGER NOT NULL,
                idw_company INTEGER NOT NULL,
                word VARCHAR(550) NOT NULL,
                repetition INTEGER NOT NULL,
                weighting INTEGER NOT NULL,
                CONSTRAINT date2 PRIMARY KEY (idw_date, idw_weighting, idw_company, word)
);


CREATE TABLE public.fact_social_status (
                idw_date DATE NOT NULL,
                idw_company INTEGER NOT NULL,
                idw_category INTEGER NOT NULL,
                idw_social_network INTEGER NOT NULL,
                likes_number INTEGER NOT NULL,
                number_unique_people INTEGER NOT NULL,
                CONSTRAINT date3 PRIMARY KEY (idw_date, idw_company, idw_category, idw_social_network)
);


ALTER TABLE public.fact_social_status ADD CONSTRAINT dim_category_fact_message_fk
FOREIGN KEY (idw_category)
REFERENCES public.dim_category (idw_category)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fact_word ADD CONSTRAINT dim_weighting_fact_message_fk
FOREIGN KEY (idw_weighting)
REFERENCES public.dim_weighting (idw_weighting)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fact_social_status ADD CONSTRAINT dim_social_network_fact_message_fk
FOREIGN KEY (idw_social_network)
REFERENCES public.dim_social_network (idw_social_network)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fact_social_status ADD CONSTRAINT dim_user_fact_message_fk
FOREIGN KEY (idw_company)
REFERENCES public.dim_company (idw_company)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fact_word ADD CONSTRAINT dim_company_fact_word_fk
FOREIGN KEY (idw_company)
REFERENCES public.dim_company (idw_company)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fact_social_status ADD CONSTRAINT dim_time_fact_message_fk
FOREIGN KEY (idw_date)
REFERENCES public.dim_time (idw_date)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fact_word ADD CONSTRAINT dim_time_fact_message_fk1
FOREIGN KEY (idw_date)
REFERENCES public.dim_time (idw_date)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fact_dictionary ADD CONSTRAINT dim_time_fact_dictionary_fk
FOREIGN KEY (idw_date)
REFERENCES public.dim_time (idw_date)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;