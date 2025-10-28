--
-- PostgreSQL database dump
--

\restrict 7MrcLPuixxT5gNTa4eeHqKPlQkVuoM7lXv92rxUPMOjtiZ7YLftIF3cZkRFJLDp

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-28 12:32:38

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3503 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 226 (class 1259 OID 32822)
-- Name: actividad; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actividad (
    id integer NOT NULL,
    nombre character varying,
    requiere_talle boolean,
    edad_minima integer,
    descripcion character varying
);


ALTER TABLE public.actividad OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 32821)
-- Name: actividad_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.actividad_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.actividad_id_seq OWNER TO postgres;

--
-- TOC entry 3504 (class 0 OID 0)
-- Dependencies: 225
-- Name: actividad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.actividad_id_seq OWNED BY public.actividad.id;


--
-- TOC entry 219 (class 1259 OID 32781)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 32813)
-- Name: estado_horario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estado_horario (
    nombre character varying NOT NULL,
    descripcion character varying
);


ALTER TABLE public.estado_horario OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 32844)
-- Name: horario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horario (
    id integer NOT NULL,
    id_actividad integer,
    hora_inicio character varying,
    hora_fin character varying,
    cupo_total integer,
    cupo_ocupado integer,
    estado character varying,
    fecha date
);


ALTER TABLE public.horario OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 32843)
-- Name: horario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.horario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.horario_id_seq OWNER TO postgres;

--
-- TOC entry 3505 (class 0 OID 0)
-- Dependencies: 229
-- Name: horario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.horario_id_seq OWNED BY public.horario.id;


--
-- TOC entry 232 (class 1259 OID 32865)
-- Name: inscripcion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inscripcion (
    id integer NOT NULL,
    id_horario integer,
    id_visitante integer,
    nro_personas integer,
    "acepta_Terminos_Condiciones" boolean
);


ALTER TABLE public.inscripcion OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 32864)
-- Name: inscripcion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.inscripcion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inscripcion_id_seq OWNER TO postgres;

--
-- TOC entry 3506 (class 0 OID 0)
-- Dependencies: 231
-- Name: inscripcion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.inscripcion_id_seq OWNED BY public.inscripcion.id;


--
-- TOC entry 223 (class 1259 OID 32803)
-- Name: parque; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parque (
    id integer NOT NULL,
    horario_abrir_puertas character varying,
    horario_cerrar_puertas character varying,
    abierto boolean
);


ALTER TABLE public.parque OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 32802)
-- Name: parque_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parque_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parque_id_seq OWNER TO postgres;

--
-- TOC entry 3507 (class 0 OID 0)
-- Dependencies: 222
-- Name: parque_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parque_id_seq OWNED BY public.parque.id;


--
-- TOC entry 221 (class 1259 OID 32788)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying,
    email character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 32787)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 3508 (class 0 OID 0)
-- Dependencies: 220
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 228 (class 1259 OID 32833)
-- Name: visitante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.visitante (
    id integer NOT NULL,
    nombre character varying,
    dni integer,
    edad integer,
    talle character varying
);


ALTER TABLE public.visitante OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 32832)
-- Name: visitante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.visitante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.visitante_id_seq OWNER TO postgres;

--
-- TOC entry 3509 (class 0 OID 0)
-- Dependencies: 227
-- Name: visitante_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.visitante_id_seq OWNED BY public.visitante.id;


--
-- TOC entry 3303 (class 2604 OID 32825)
-- Name: actividad id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actividad ALTER COLUMN id SET DEFAULT nextval('public.actividad_id_seq'::regclass);


--
-- TOC entry 3305 (class 2604 OID 32847)
-- Name: horario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horario ALTER COLUMN id SET DEFAULT nextval('public.horario_id_seq'::regclass);


--
-- TOC entry 3306 (class 2604 OID 32868)
-- Name: inscripcion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion ALTER COLUMN id SET DEFAULT nextval('public.inscripcion_id_seq'::regclass);


--
-- TOC entry 3302 (class 2604 OID 32806)
-- Name: parque id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parque ALTER COLUMN id SET DEFAULT nextval('public.parque_id_seq'::regclass);


--
-- TOC entry 3301 (class 2604 OID 32791)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3304 (class 2604 OID 32836)
-- Name: visitante id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visitante ALTER COLUMN id SET DEFAULT nextval('public.visitante_id_seq'::regclass);


--
-- TOC entry 3491 (class 0 OID 32822)
-- Dependencies: 226
-- Data for Name: actividad; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.actividad (id, nombre, requiere_talle, edad_minima, descripcion) VALUES (3161, 'Tirolesa', true, 12, 'Deslízate por las copas de los árboles en una experiencia emocionante de aventura extrema');
INSERT INTO public.actividad (id, nombre, requiere_talle, edad_minima, descripcion) VALUES (3162, 'Safari', false, NULL, 'Recorre el parque en vehículos especiales y observa la fauna local en su hábitat natural');
INSERT INTO public.actividad (id, nombre, requiere_talle, edad_minima, descripcion) VALUES (3163, 'Palestra', true, 8, 'Zona de juegos infantiles con estructuras');
INSERT INTO public.actividad (id, nombre, requiere_talle, edad_minima, descripcion) VALUES (3164, 'Jardineria', false, NULL, 'Aprende técnicas de cultivo sustentable y participa en el cuidado de nuestro vivero ecológico');


--
-- TOC entry 3484 (class 0 OID 32781)
-- Dependencies: 219
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version (version_num) VALUES ('fb528749b4f4');


--
-- TOC entry 3489 (class 0 OID 32813)
-- Dependencies: 224
-- Data for Name: estado_horario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.estado_horario (nombre, descripcion) VALUES ('activo', 'Horario activo');
INSERT INTO public.estado_horario (nombre, descripcion) VALUES ('inactivo', 'Horario inactivo');


--
-- TOC entry 3495 (class 0 OID 32844)
-- Dependencies: 230
-- Data for Name: horario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3286, 3163, '15:00', '16:00', 8, 1, 'activo', NULL);
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3282, 3161, '10:00', '11:00', 5, 5, 'activo', NULL);
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3284, 3163, '13:00', '14:00', 8, 2, 'activo', '2025-10-24');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3287, 3161, '08:00', '09:00', 20, 0, 'activo', '2025-10-24');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3288, 3162, '09:00', '10:00', 15, 0, 'activo', '2025-10-24');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3289, 3163, '11:00', '12:00', 25, 3, 'activo', '2025-10-24');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3290, 3164, '16:00', '17:00', 30, 0, 'activo', '2025-10-24');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3291, 3161, '09:00', '10:00', 10, 0, 'activo', '2025-10-25');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3292, 3162, '10:00', '11:00', 15, 2, 'activo', '2025-10-25');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3293, 3164, '14:00', '15:00', 20, 0, 'activo', '2025-10-25');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3294, 3161, '15:00', '16:00', 25, 5, 'activo', '2025-10-25');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3296, 3161, '09:00', '10:00', 30, 0, 'activo', '2025-10-28');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3297, 3162, '08:00', '09:00', 15, 0, 'activo', '2025-10-28');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3298, 3163, '10:00', '11:00', 20, 0, 'activo', '2025-10-28');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3299, 3164, '11:00', '12:00', 20, 0, 'activo', '2025-10-28');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3300, 3161, '12:00', '13:00', 10, 1, 'activo', '2025-10-28');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3301, 3162, '14:00', '15:00', 15, 0, 'activo', '2025-11-05');
-- INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3302, 3163, '14:00', '15:00', 15, 0, 'activo', '2025-11-05'); -- ELIMINADO POR CONFLICTO
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3303, 3164, '15:00', '16:00', 28, 0, 'activo', '2025-11-05');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3304, 3161, '16:00', '17:00', 25, 0, 'activo', '2025-11-05');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3305, 3162, '17:00', '18:00', 10, 0, 'activo', '2025-11-05');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3306, 3163, '19:00', '20:00', 20, 0, 'activo', '2025-11-05');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3307, 3161, '08:00', '09:00', 15, 0, 'activo', '2025-11-15');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3308, 3162, '09:00', '10:00', 15, 0, 'activo', '2025-11-15');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3310, 3164, '11:00', '12:00', 15, 0, 'activo', '2025-11-15');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3311, 3161, '12:00', '13:00', 22, 2, 'activo', '2025-11-15');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3312, 3162, '13:00', '14:00', 20, 0, 'activo', '2025-11-15');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3313, 3163, '14:00', '15:00', 20, 0, 'activo', '2025-11-15');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3314, 3164, '09:00', '10:00', 30, 10, 'activo', '2025-11-24');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3315, 3161, '10:00', '11:00', 20, 0, 'activo', '2025-11-24');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3316, 3162, '16:00', '17:00', 10, 0, 'activo', '2025-11-24');
INSERT INTO public.horario (id, id_actividad, hora_inicio, hora_fin, cupo_total, cupo_ocupado, estado, fecha) VALUES (3285, 3164, '14:00', '15:00', 10, 0, 'activo', NULL);

--
-- TOC entry 3497 (class 0 OID 32865)
-- Dependencies: 232
-- Data for Name: inscripcion; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.inscripcion (id, id_horario, id_visitante, nro_personas, "acepta_Terminos_Condiciones") VALUES (507, 3286, 1947, 1, true);
INSERT INTO public.inscripcion (id, id_horario, id_visitante, nro_personas, "acepta_Terminos_Condiciones") VALUES (508, 3282, 1947, 1, true);
INSERT INTO public.inscripcion (id, id_horario, id_visitante, nro_personas, "acepta_Terminos_Condiciones") VALUES (509, 3282, 1948, 1, true);
INSERT INTO public.inscripcion (id, id_horario, id_visitante, nro_personas, "acepta_Terminos_Condiciones") VALUES (510, 3282, 1949, 1, true);
INSERT INTO public.inscripcion (id, id_horario, id_visitante, nro_personas, "acepta_Terminos_Condiciones") VALUES (511, 3282, 1950, 1, true);
INSERT INTO public.inscripcion (id, id_horario, id_visitante, nro_personas, "acepta_Terminos_Condiciones") VALUES (512, 3282, 1951, 1, true);
INSERT INTO public.inscripcion (id, id_horario, id_visitante, nro_personas, "acepta_Terminos_Condiciones") VALUES (513, 3284, 1947, 1, true);
INSERT INTO public.inscripcion (id, id_horario, id_visitante, nro_personas, "acepta_Terminos_Condiciones") VALUES (514, 3284, 1952, 1, true);


--
-- TOC entry 3488 (class 0 OID 32803)
-- Dependencies: 223
-- Data for Name: parque; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3486 (class 0 OID 32788)
-- Dependencies: 221
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3493 (class 0 OID 32833)
-- Dependencies: 228
-- Data for Name: visitante; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1947, 'Emmanuel Chaile', 11111111, 25, 'XL');
INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1948, 'Emmmanuel Chaile', 11111112, 25, 'XL');
INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1949, 'Emmanuel Chaile', 11111113, 25, 'S');
INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1950, 'ech', 11111114, 99, 'XL');
INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1951, 'ech', 11111115, 25, 'M');
INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1952, 'ech', 11111118, 9, 'S');
INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1944, 'Ana', 12345678, 25, 'M');
INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1945, 'Luis', 87654321, 30, 'L');
INSERT INTO public.visitante (id, nombre, dni, edad, talle) VALUES (1946, 'SinTalle', 12121212, 10, NULL);


--
-- TOC entry 3510 (class 0 OID 0)
-- Dependencies: 225
-- Name: actividad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.actividad_id_seq', 3164, true);


--
-- TOC entry 3511 (class 0 OID 0)
-- Dependencies: 229
-- Name: horario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.horario_id_seq', 3316, true);


--
-- TOC entry 3512 (class 0 OID 0)
-- Dependencies: 231
-- Name: inscripcion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.inscripcion_id_seq', 514, true);


--
-- TOC entry 3513 (class 0 OID 0)
-- Dependencies: 222
-- Name: parque_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parque_id_seq', 1, false);


--
-- TOC entry 3514 (class 0 OID 0)
-- Dependencies: 220
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- TOC entry 3515 (class 0 OID 0)
-- Dependencies: 227
-- Name: visitante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.visitante_id_seq', 1952, true);


--
-- TOC entry 3322 (class 2606 OID 32830)
-- Name: actividad actividad_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actividad
    ADD CONSTRAINT actividad_pkey PRIMARY KEY (id);


--
-- TOC entry 3308 (class 2606 OID 32786)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3320 (class 2606 OID 32820)
-- Name: estado_horario estado_horario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estado_horario
    ADD CONSTRAINT estado_horario_pkey PRIMARY KEY (nombre);


--
-- TOC entry 3328 (class 2606 OID 32852)
-- Name: horario horario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horario
    ADD CONSTRAINT horario_pkey PRIMARY KEY (id);


--
-- TOC entry 3331 (class 2606 OID 32871)
-- Name: inscripcion inscripcion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion
    ADD CONSTRAINT inscripcion_pkey PRIMARY KEY (id);


--
-- TOC entry 3318 (class 2606 OID 32811)
-- Name: parque parque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parque
    ADD CONSTRAINT parque_pkey PRIMARY KEY (id);


--
-- TOC entry 3313 (class 2606 OID 32798)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3315 (class 2606 OID 32796)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3326 (class 2606 OID 32841)
-- Name: visitante visitante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visitante
    ADD CONSTRAINT visitante_pkey PRIMARY KEY (id);


--
-- TOC entry 3323 (class 1259 OID 32831)
-- Name: ix_actividad_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_actividad_id ON public.actividad USING btree (id);


--
-- TOC entry 3329 (class 1259 OID 32863)
-- Name: ix_horario_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_horario_id ON public.horario USING btree (id);


--
-- TOC entry 3332 (class 1259 OID 32882)
-- Name: ix_inscripcion_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_inscripcion_id ON public.inscripcion USING btree (id);


--
-- TOC entry 3316 (class 1259 OID 32812)
-- Name: ix_parque_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_parque_id ON public.parque USING btree (id);


--
-- TOC entry 3309 (class 1259 OID 32801)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 3310 (class 1259 OID 32799)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- TOC entry 3311 (class 1259 OID 32800)
-- Name: ix_users_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_name ON public.users USING btree (name);


--
-- TOC entry 3324 (class 1259 OID 32842)
-- Name: ix_visitante_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_visitante_id ON public.visitante USING btree (id);


--
-- TOC entry 3333 (class 2606 OID 32853)
-- Name: horario horario_estado_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horario
    ADD CONSTRAINT horario_estado_fkey FOREIGN KEY (estado) REFERENCES public.estado_horario(nombre);


--
-- TOC entry 3334 (class 2606 OID 32858)
-- Name: horario horario_id_actividad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horario
    ADD CONSTRAINT horario_id_actividad_fkey FOREIGN KEY (id_actividad) REFERENCES public.actividad(id);


--
-- TOC entry 3335 (class 2606 OID 32872)
-- Name: inscripcion inscripcion_id_horario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion
    ADD CONSTRAINT inscripcion_id_horario_fkey FOREIGN KEY (id_horario) REFERENCES public.horario(id);


--
-- TOC entry 3336 (class 2606 OID 32877)
-- Name: inscripcion inscripcion_id_visitante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion
    ADD CONSTRAINT inscripcion_id_visitante_fkey FOREIGN KEY (id_visitante) REFERENCES public.visitante(id);


-- Completed on 2025-10-28 12:32:38

--
-- PostgreSQL database dump complete
--

\unrestrict 7MrcLPuixxT5gNTa4eeHqKPlQkVuoM7lXv92rxUPMOjtiZ7YLftIF3cZkRFJLDp

