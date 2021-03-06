-- KPO data system data model
-- author: Jorge Gil, 2017


-- object: datasysteem | type: SCHEMA --
-- DROP SCHEMA IF EXISTS datasysteem CASCADE;
CREATE SCHEMA datasysteem;
ALTER SCHEMA datasysteem OWNER TO postgres;

-- DROP TABLE IF EXISTS datasysteem.woonscenarios CASCADE;
CREATE TABLE datasysteem.woonscenarios(
	sid serial NOT NULL,
	geom geometry(MultiPolygon,28992),
	code character varying,
	plaatsnaam character varying,
	scenario_naam character varying,
	op_loopafstand boolean,
	op_fietsafstand boolean,
	dichtstbijzijnde_station character varying,
	huishoudens integer,
	area double precision,
	dichtheid double precision,
	nieuwe_huishoudens integer,
	procentuele_verandering double precision,
	CONSTRAINT woonscenarios_pk PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.overzicht_woonscenarios CASCADE;
CREATE TABLE datasysteem.overzicht_woonscenarios(
	sid serial NOT NULL,
	scenario_naam character varying,
	tod_beleidsniveau smallint,
	verwachte_huishoudens integer,
	op_loopafstand integer,
	op_fietsafstand integer,
	buiten_invloedsgebied integer,
	CONSTRAINT overzicht_woonscenarios_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.knooppunten CASCADE;
CREATE TABLE datasysteem.knooppunten(
	sid serial NOT NULL,
	geom geometry(MultiPoint,28992),
	station_vdm_code character varying,
	station_naam character varying,
	halte_id character varying,
	halte_naam character varying,
	huishoudens integer,
	passanten integer,
	in_uit_trein integer,
	overstappers integer,
	in_uit_btm integer,
	btm_voortransport double precision,
	btm_natransport double precision,
	lopen_voortransport double precision,
	lopen_natransport double precision,
	fiets_voortransport double precision,
	fiets_natransport double precision,
	pr_voortransport double precision,
	pr_natransport double precision,
	fiets_plaatsen integer,
	fiets_bezetting double precision,
	ov_fietsen integer,
	pr_plaatsen integer,
	pr_bezetting double precision,
	ov_routes character varying,
	CONSTRAINT knooppunten_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.knooppuntenscenarios CASCADE;
CREATE TABLE datasysteem.knooppuntenscenarios(
	sid serial NOT NULL,
	geom geometry(MultiPoint,28992),
	station_vdm_code character varying,
	station_naam character varying,
	halte_id character varying,
	halte_naam character varying,
	scenario_naam character varying,
	tod_beleidsniveau smallint,
	huishoudens integer,
	nieuwe_huishoudens integer,
	procent_huis_verandering double precision,
	procent_locale_reizigers double precision,
	procent_knoop_verandering double precision,
	in_uit_trein integer,
	in_uit_btm integer,
	fiets_plaatsen integer,
	fiets_bezetting integer,
	pr_plaatsen integer,
	pr_bezetting integer,
	CONSTRAINT knooppuntenscenarios_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.ruimtelijke_kenmerken CASCADE;
CREATE TABLE datasysteem.ruimtelijke_kenmerken(
	sid serial NOT NULL,
	geom geometry(MultiPolygon,28992),
	cell_id character varying,
	huishoudens integer,
	intensiteit integer,
	fysieke_dichtheid double precision,
	woz_waarde double precision,
	ov_bereikbaarheidsniveau character varying,
	ov_bereikbaarheidsindex double precision,
	gemeente character varying,
	CONSTRAINT ruimtelijke_kenmerken_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.ontwikkellocaties CASCADE;
CREATE TABLE datasysteem.ontwikkellocaties(
	sid serial NOT NULL,
	geom geometry(MultiPolygon,28992),
	plan_naam character varying,
	plan_id character varying,
	gemeente character varying,
	plaatsnaam character varying,
	adres character varying,
	bestaande_woningen integer,
	geplande_woningen integer,
	net_nieuwe_woningen integer,
	vlakte double precision,
	dichtheid double precision,
	gemiddelde_huishoudens double precision,
	gemiddelde_intensiteit double precision,
	gemiddelde_dichtheid double precision,
	gemiddelde_woz double precision,
	gemiddelde_bereikbaarheidsindex double precision,
	bereikbaare_locatie boolean,
	cell_ids character varying,
	CONSTRAINT ontwikkellocaties_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.invloedsgebied_overlap CASCADE;
CREATE TABLE datasysteem.invloedsgebied_overlap(
	sid serial NOT NULL,
	geom geometry(MultiPolygon,28992),
	huishoudens integer,
	intensiteit integer,
	station_namen character varying,
	station_aantal smallint,
	ov_routes_ids character varying,
	CONSTRAINT invloedsgebied_overlap_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.belangrijke_locaties CASCADE;
CREATE TABLE datasysteem.belangrijke_locaties(
	sid serial NOT NULL,
	geom geometry(MultiPolygon,28992),
	locatie_id character varying,
	locatie_naam character varying,
	op_loopafstand boolean,
	station_namen character varying,
	ov_routes_ids character varying,
	CONSTRAINT belangrijke_locaties_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.magneten CASCADE;
CREATE TABLE datasysteem.magneten(
	sid serial NOT NULL,
	geom geometry(MultiPoint,28992),
	locatie_kwaliteit integer,
	locatie_naam character varying,
	op_loopafstand boolean,
	op_fietsafstand boolean,
	op_ovafstand boolean,
	station_namen character varying,
	ov_routes_ids character varying,
	CONSTRAINT regionale_voorzieningen_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.fietsroutes CASCADE;
CREATE TABLE datasysteem.fietsroutes(
	sid serial NOT NULL,
	geom geometry(Linestring,28992),
	route_id character varying,
	route_intensiteit integer,
	station_naam character varying,
	invloedsgebied_ids character varying,
	CONSTRAINT fietsroutes_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.ov_routes CASCADE;
CREATE TABLE datasysteem.ov_routes(
	sid serial NOT NULL,
	geom geometry(Linestring,28992),
	route_id character varying,
	route_naam character varying,
	modaliteit character varying,
	ochtendspits double precision,
	daluren double precision,
	avondspits double precision,
	CONSTRAINT ov_routes_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.isochronen CASCADE;
CREATE TABLE datasysteem.isochronen(
	sid serial NOT NULL,
	geom geometry(MultiPolygon,28992),
	halte_id character varying,
	halte_naam character varying,
	halte_modaliteit character varying,
	modaliteit character varying,
	isochroon_afstand smallint,
	CONSTRAINT isochronen_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.isochronen_expanded CASCADE;
CREATE TABLE datasysteem.isochronen_expanded(
	sid serial NOT NULL,
	geom geometry(MultiPolygon,28992),
	halte_id character varying,
	halte_naam character varying,
	halte_modaliteit character varying,
	modaliteit character varying,
	isochroon_afstand smallint,
	CONSTRAINT isochronen_expanded_pkey PRIMARY KEY (sid)
);

-- DROP TABLE IF EXISTS datasysteem.ov_haltes CASCADE;
CREATE TABLE datasysteem.ov_haltes(
	sid serial NOT NULL,
	geom geometry(Point,28992),
	halte_id character varying,
	halte_zone integer,
	halte_naam character varying,
	halte_gemeente character varying,
	tram boolean,
	metro boolean,
	trein boolean,
	bus boolean,
	veerboot boolean,
	bus_ochtendspits double precision,
	bus_daluren double precision,
	bus_avondspits double precision,
	tram_ochtendspits double precision,
	tram_daluren double precision,
	tram_avondspits double precision,
	metro_ochtendspits double precision,
	metro_daluren double precision,
	metro_avondspits double precision,
	veerboot_ochtendspits double precision,
	veerboot_daluren double precision,
	veerboot_avondspits double precision,
	trein_ochtendspits double precision,
	trein_daluren double precision,
	trein_avondspits double precision,
	hsl_ochtendspits double precision,
	hsl_daluren double precision,
	hsl_avondspits double precision,
	ic_ochtendspits double precision,
	ic_daluren double precision,
	ic_avondspits double precision,
	spr_ochtendspits double precision,
	spr_daluren double precision,
	spr_avondspits double precision,
	CONSTRAINT ov_haltes_pkey PRIMARY KEY (sid)
);