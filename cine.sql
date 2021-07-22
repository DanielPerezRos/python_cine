-- biografia definition

CREATE TABLE biografia(
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    texto text NOT NULL
 );


-- countries definition

CREATE TABLE countries(
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name varchar(50) NULL,
    capital varchar(50) NULL,
    continent varchar(50) NULL,
    national_flag varchar(100) NULL
);


-- genres definition

CREATE TABLE genres(
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name varchar(30) NULL,
    description text NULL
);


-- lugares definition

CREATE TABLE lugares(
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    pais text NULL,
    ciudad text NULL,
    paraje text NULL
);


-- actor definition

CREATE TABLE actor(
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    nombre varchar(10) NOT NULL,
    apellidos varchar(25) NOT NULL,
    foto varchar(100) NOT NULL UNIQUE,
    nacimiento date NOT NULL,
    biografia_id bigint NOT NULL UNIQUE REFERENCES biografia (id) DEFERRABLE INITIALLY DEFERRED,
    pais_id bigint NOT NULL REFERENCES countries (id) DEFERRABLE INITIALLY DEFERRED
);

-- director definition

CREATE TABLE director(
id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    nombre varchar(10) NOT NULL,
    apellidos varchar(25) NOT NULL,
    foto varchar(100) NOT NULL UNIQUE,
    nacimiento date NOT NULL,
    biografia_id bigint NOT NULL UNIQUE REFERENCES biografia (id) DEFERRABLE INITIALLY DEFERRED,
    pais_id bigint NOT NULL REFERENCES countries (id) DEFERRABLE INITIALLY DEFERRED
);

-- studios definition

CREATE TABLE studios(
id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name varchar(50) NULL,
    president varchar(50) NULL,
    foundation integer NULL,
    logo varchar(100) NULL,
    country_id bigint NULL REFERENCES countries (id) DEFERRABLE INITIALLY DEFERRED
);

-- movies definition

CREATE TABLE movies(
id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name varchar(50) NULL,
    description text NULL,
    image varchar(100) NULL,
    cost integer NULL,
    income integer NULL,
    date date NULL,
    country_id bigint NULL REFERENCES countries (id) DEFERRABLE INITIALLY DEFERRED,
    director_id bigint NULL REFERENCES director (id) DEFERRABLE INITIALLY DEFERRED,
    studio_id bigint NULL REFERENCES studios (id) DEFERRABLE INITIALLY DEFERRED
);