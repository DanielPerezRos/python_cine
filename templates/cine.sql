/*use cine;*/

create table Pais(
	id int primary key auto_increment,
    nombre varchar(50),
    continente varchar(20)
);

create table Persona(
	id int primary key auto_increment,
	nombre varchar(10),
	apellidos varchar(25),
	foto varchar(255),
	pais int,
    nacimiento date,
    foreign key (pais) references Pais(id)
);

create table Genero(
    id int primary key auto_increment,
    nombre VARCHAR(10),
    descripcion VARCHAR(255)
);

create table Estudio(
    id int primary key auto_increment,
    nombre VARCHAR(30),
    pais int,
    presidente int,
    fundacion date,
    foreign key (presidente) references Persona(id),
    foreign key (pais) references Pais(id)
);

create table Rodaje(
    id int primary key auto_increment,
    nombre varchar(50),
    pais int,
    foreign key(pais) references Pais(id)
);

CREATE TABLE Pelicula(
    id int primary key auto_increment,
    nombre varchar(20),
    genero int,
    descripcion varchar(255),
    foto VARCHAR(255),
    pais int,
	protagonista int,
	director int,
    estudio int,
    coste int,
    recaudacion int,
    foreign key (protagonista) references Persona(id),
    foreign key (director) references Persona(id),
    foreign key (pais) references Pais(id),
    foreign key (genero) references Genero(id),
    foreign key (estudio) references Estudio(id)
);

create table Rodada(
    id int primary key auto_increment,
    lugar int,
    pelicula int,
    foreign key (lugar) references Rodaje(id),
    foreign key (pelicula) references Pelicula(id)
);

create table Lugares(
    id int primary key,
    pais int,
    ciudad VARCHAR(60),
    paraje VARCHAR(90),
);
