/*Crea la base de datos ---------------------------------------------------------------------------------------*/

-- create database Proyecto_BD;

	/*Checks*/
	/*Clave primaria*/
	/*Claves foraneas*/

--Entidades sin claves foráneas------------------------------------------------------------------------------------------

create table Stud(
	S_Clave				serial NOT NULL UNIQUE,
	S_Nombre			varchar(45) NOT NULL,
	S_Fecha_Creacion	date NOT NULL,
	/*Clave primaria*/
	constraint PK_Stud primary key (S_Clave)
);

create table Tipo_Usuario(
	TU_Clave		serial not null  unique,
	TU_Nombre		Varchar(45) not null,
	/*Clave primaria*/
	constraint PK_Tipo_Usuario primary key(TU_Clave)
);

create table Accion(
	ACC_Clave							serial not null  unique,
	ACC_Nombre						varchar(45) NOT NULL,
	ACC_Tabla_Objetivo		varchar(45) NOT NULL,
	/*Clave primaria*/
	constraint PK_Accion primary key(ACC_Clave)
);

create table Color(
	COL_Clave		serial NOT NULL,
	COL_Nombre 		varchar(45) NOT NULL,
	/*Clave primaria*/
	constraint PK_Color primary key (COL_Clave)
);

create table Tipo_Medicamento(
	TM_Clave	serial NOT NULL UNIQUE,
	TM_Nombre	varchar(20) NOT NULL,
	/*Clave primaria*/
	constraint PK_tipoMedicamento primary key(TM_Clave)
);

create	table Categoria_Carrera(
	CA_Clave			serial NOT NULL UNIQUE,
	CA_Nombre			varchar(20) NOT NULL,
	/*Clave primaria*/
	constraint PK_Categoria_Carrera primary key(CA_Clave),
	/*Check*/
	constraint Check_Categoria_Carrera_Nombre Check (CA_Nombre IN ('Normal','Clasico','Copa')) 
);

create	table Tipo_Carrera(
	TC_Clave						serial NOT NULL UNIQUE,
	TC_Nombre						varchar(60) NOT NULL,
	TC_Sexo							varchar(1),
	TC_Edad_Minima			Numeric(4),
	TC_Edad_Maxima			Numeric(4),
	TC_Victoria_Minima	Numeric(4),
	TC_Victoria_Maxima	Numeric(4),
	/*Clave primaria*/
	constraint PK_Tipo_Carrera primary key(TC_Clave),
	/*Checks*/
	constraint Check_Tipo_Carrera_Sexo Check (TC_Sexo IN ('Y','C')) 
);

create	table Porcentaje_Dividendo(
	PD_Clave			serial NOT NULL UNIQUE,
	PD_Puesto			numeric(3) NOT NULL,
	PD_Porcentaje		numeric(3,2)	NOT NULL,
	/*Clave primaria*/
	constraint PK_Porcentaje_Dividendo primary key(PD_Clave)
);

create	table Causa_Retiro(
	CR_Clave				serial NOT NULL UNIQUE,
	CR_Descripcion	varchar(45)	NOT NULL,
	CR_Nombre				varchar(45) NOT NULL,
	CR_Duracion			numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Causa_Retiro  primary key (CR_Clave)
);

create table Implemento(
	I_Codigo				serial NOT NULL UNIQUE,
	I_Nombre				varchar(45)	NOT NULL,
	I_Diminutivo		varchar(3) NOT NULL,
	/*Clave primaria*/
	constraint PK_Implemento  primary key (I_Codigo),
	/*Checks*/
	constraint Check_Implemento_Nombre Check (I_Nombre IN ('Gringola','Lengua Amarrada','Bozal','Bozal Lenguero',
		'Bozal Blanco Nose Band','Martingala','Preta','Guayo','Vendas','Orejas Tapadas','Latigo','Casquillos Correctivos',
		'Casquillos de Hierro') ),
	constraint Check_Implemento_Diminutivo Check (I_Diminutivo IN ('GR','CC','CH','LA','BZ','BL','BB','M','P','G','V','OT','L') )
);

create Table Tipo_Apuesta(
	TA_Clave							serial not null unique,
	TA_Nombre							Varchar(20) not null,
	TA_Precio							Decimal(6,2) not null,
	TA_Saldo_Minimo						Decimal(6,2),
	TA_Precio_Jugada_Adicional			Numeric(10,2),
	TA_Cant_Caballo_Minimo_Carrera		Numeric(3),
	TA_Num_Ejemplar_Minimo_Necesario	Numeric(3),
	/*Clave primaria*/
	constraint PK_Tipo_Apuesta primary key(TA_Clave)
);

create table Metodo_Pago(
	MP_Clave 	serial not null unique,
	MP_Nombre	varchar(56),
	/*Clave primaria*/
	constraint PK_Metodo_Pago primary key(MP_Clave)
);

--Entidades con claves foráneas------------------------------------------------------------------------------------------

create table Lugar(
	L_Clave		 serial NOT NULL UNIQUE,
	L_Nombre 	 varchar(45) NOT NULL,
	L_Tipo 		 varchar(45) NOT NULL,
	FK_Lugar 	 integer,
	/*Checks*/
	constraint Check_Lugar_Tipo CHECK (L_Tipo in ('Estado','Municipio','Parroquia')),
	/*Clave primaria*/
	constraint PK_Lugar primary key (L_Clave),
	/*Claves foraneas*/
	constraint fk_Lugar foreign key (FK_Lugar) references Lugar(L_Clave)
);

create table Haras(
	H_Clave 	serial NOT NULL UNIQUE,
	H_Nombre 	varchar(45) NOT NULL,
	FK_Lugar	integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Haras primary key (H_Clave),
	/*Claves foraneas*/
	constraint fk_Lugar foreign key (FK_Lugar) references Lugar(L_Clave)
);

create table Hipodromo(
	H_ID						serial NOT NULL UNIQUE,
	H_Nombre 					varchar(45) NOT NULL UNIQUE,
	H_Direccion					varchar(100) NOT NULL UNIQUE,
	H_Fecha_Creacion 			date NOT NULL,
	H_Descripcion_Historica 	text NOT NULL UNIQUE,
	FK_Lugar 					integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Hipodromo primary key (H_ID),
	/*Claves foraneas*/
	constraint fk_Lugar foreign key (FK_Lugar) references Lugar(L_Clave)
);

create table Caballeriza(
	CA_Clave 			serial NOT NULL UNIQUE,
	CA_Numero 			numeric(10)	NOT NULL,
	CA_Capacidad		numeric(10) NOT NULL,
	FK_Hipodromo		integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Caballeriza primary key (CA_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Puesto(
	PU_Clave				serial NOT NULL UNIQUE,
	PU_Numero				numeric(10) NOT NULL,
	FK_Caballeriza			integer NOT NULL,
	/*Checks*/
	constraint Check_Puesto_Numero CHECK (PU_Numero between 1 and 50),
	/*Clave primaria*/
	constraint PK_Puesto primary key (PU_Clave),
	/*Claves foraneas*/
	constraint fk_Caballeriza foreign key (FK_Caballeriza) references Caballeriza(CA_Clave)
);

create table Ejemplar(
  E_Tatuaje_Labial    numeric(10) NOT NULL UNIQUE,
  E_Nombre            varchar(45) NOT NULL,
  E_Color_Pelaje      varchar(45) NOT NULL,
  E_Sexo              varchar(10) NOT NULL,
  E_Fecha_Nacimiento  date NOT NULL,
  E_Fecha_Ing_Hipo    date NOT NULL,
  E_Peso              numeric(5) NOT NULL,
  FK_Haras            integer NOT NULL,
  FK_Madre            numeric(10),
  FK_Padre            numeric(10),
  FK_Puesto           integer NOT NULL,
  FK_Caballeriza      integer NOT NULL,
  /*Checks*/
  constraint Check_Ejemplar_Color_Pelaje CHECK (E_Color_Pelaje in ('C','Z','T','A')),
  constraint Check_Ejemplar_Sexo CHECK (E_Sexo in ('Y','C')),
  /*Clave primaria*/
  constraint PK_Ejemplar primary key (E_Tatuaje_Labial),
  /*Claves foraneas*/
  constraint fk_Haras foreign key (FK_Haras) references Haras(H_Clave),
  constraint fk_Madre foreign key (FK_Madre) references Ejemplar(E_Tatuaje_Labial),
  constraint fk_Padre foreign key (FK_Padre) references Ejemplar(E_Tatuaje_Labial),
  constraint fk_Puesto foreign key (FK_Puesto) references Puesto(PU_Clave),
  constraint fk_Caballeriza foreign key (FK_Caballeriza) references Caballeriza(CA_Clave)
);

create table Aficionado(
	P_Cedula						Numeric(10)  not null unique ,
	P_Primer_Nombre			Varchar(20) not null,
	P_Segundo_Nombre		Varchar(20),
	P_Primer_Apellido		Varchar(20) not null,
	P_Segundo_Apellido	Varchar(20),
	P_Sexo							Char(1) not null,
	P_Direccion					Varchar(50) not null,
	AF_Profesion				Varchar(30),
	FK_Lugar						integer not null,
	/*Clave primaria*/
	constraint PK_Aficionado	primary key(P_Cedula),
	/*Clave foranea*/
	constraint FK_Lugar 		foreign key(FK_Lugar) references Lugar(L_Clave),
	--Check
	constraint Check_Aficionado_Sexo check(P_Sexo in('M','F'))
);

create table Entrenador(
	P_Cedula						Numeric(10) unique not null ,
	P_Primer_Nombre			Varchar(20) not null,
	P_Segundo_Nombre		Varchar(20),
	P_Primer_Apellido		Varchar(20) not null,
	P_Segundo_Apellido	Varchar(20),
	P_Sexo							Char(1) not null,
	P_Direccion					Varchar(50) not null,
	ENT_Fecha_Ing_Hipo	Date not null,
	FK_Lugar						integer not null,
	/*Clave primaria*/
	constraint PK_Entrenador	primary key(P_Cedula),
	/*Claves foraneas*/
	constraint FK_Lugar foreign key(FK_Lugar) references Lugar(L_Clave),
	--Check
	constraint Check_Entrenador_Sexo check(P_Sexo in('M','F'))
);

create table Veterinario(
	P_Cedula							Numeric(10) not null unique ,
	P_Primer_Nombre				Varchar(20) not null,
	P_Segundo_Nombre			Varchar(20),
	P_Primer_Apellido			Varchar(20) not null,
	P_Segundo_Apellido		Varchar(20),
	P_Sexo								Char(1) not null,
	P_Direccion						Varchar(50) not null,
	V_Numero_Colegiatura	Numeric(10) not null,
	FK_Lugar							integer not null,
	FK_Caballeriza				integer not null,
	/*Clave primaria*/
	constraint PK_Veterinario	primary key(P_Cedula),
	/*Claves foraneas*/
	constraint FK_Lugar 		foreign key(FK_Lugar) references Lugar(L_Clave),
	constraint FK_Caballeriza 	foreign key(FK_Caballeriza) references Caballeriza(CA_Clave),
	/*Checks*/
	constraint Check_Veterinario_Sexo check(P_Sexo in('M','F'))
);

create table Propietario(
	P_Cedula							Numeric(10) not null unique ,
	P_Primer_Nombre				Varchar(20) not null,
	P_Segundo_Nombre			Varchar(20),
	P_Primer_Apellido			Varchar(20) not null,
	P_Segundo_Apellido		Varchar(20),
	P_Sexo								Char(1) not null,
	P_Direccion						Varchar(50) not null,
	PR_Correo							Varchar(40) not null unique,
	PR_Fecha_Nacimiento		Date not null,
	FK_Lugar							integer not null,
	/*Clave primaria*/ 
	constraint PK_Propietario	primary key(P_Cedula),
	/*Claves foraneas*/
	constraint FK_Lugar foreign key(FK_Lugar) references Lugar(L_Clave),
	/*Checks*/
	constraint Check_Propietario_Sexo check (P_Sexo in('M','F'))
);

create table Jinete(
	P_Cedula						Numeric(10) not null unique ,
	P_Primer_Nombre			Varchar(20) not null,
	P_Segundo_Nombre		Varchar(20),
	P_Primer_Apellido		Varchar(20) not null,
	P_Segundo_Apellido	Varchar(20),
	P_Sexo							Char(1) not null,
	P_Direccion					Varchar(50) not null,
	J_Altura						Numeric(3,2) not null,
	J_Peso_Al_Ingresar	Numeric(2) not null,
	J_Peso_Actual				Numeric(2) not null,
	J_Rango							Varchar(15),
	J_Fecha_Nacimiento	Date not null,
	FK_Lugar						integer not null,
	/*Clave primaria*/
	constraint PK_Jinete primary key(P_Cedula),
	/*Clave foranea*/
	constraint FK_Lugar foreign key(FK_Lugar) references Lugar(L_Clave),
	/*Checks*/
	constraint Check_Jinete_Sexo 	check(P_Sexo in('M','F')),
	constraint Check_Jinete_Rango 	check(J_Rango in('APRENDIZ','PROFESIONAL'))
);

create table Binomio(
	BI_Clave 					serial NOT NULL UNIQUE,
	FK_Ejemplar				numeric(10) NOT NULL,
	FK_Jinete					numeric(10) NOT NULL,
	BI_Jinete_Peso		numeric(10) NOT NULL,
	BI_Ejemplar_Peso 	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Binomio primary key (BI_Clave),
	/*Claves foraneas*/
	constraint fk_Ejemplar foreign key (FK_Ejemplar) references Ejemplar(E_Tatuaje_Labial),
	constraint fk_Jinete foreign key (FK_Jinete) references Jinete(P_Cedula)
);

create table Grada(
	G_Clave				serial NOT NULL UNIQUE,
	G_Nombre			varchar(45) NOT NULL,
	G_Capacidad		numeric(5)	NOT NULL,
	FK_Hipodromo	integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Grada primary key (G_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Entrada(
	EN_Clave 									serial NOT NULL UNIQUE,
	EN_Letra_Identificacion		char(1) NOT NULL,
	EN_Zona 									varchar(45) NOT NULL,
	FK_Grada									integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Entrada primary key (EN_Clave),
	/*Claves foraneas*/
	constraint fk_Grada foreign key (FK_Grada) references Grada(G_Clave)
);

create table Estacionamiento(
	E_Clave							serial NOT NULL UNIQUE,
	E_Capacidad_Total		numeric(4) NOT NULL,
	FK_Entrada					integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Estacionamiento primary key (E_Clave),
	/*Claves foraneas*/
	constraint fk_Entrada foreign key (FK_Entrada) references Entrada(EN_Clave)
);

create table Nivel(
	NI_Clave				serial NOT NULL UNIQUE,
	NI_Apartado_4P	numeric(3) NOT NULL,
	NI_Apartado_6P	numeric(3) NOT NULL,
	NI_Apartado_8P	numeric(3) NOT NULL,
	FK_Grada				integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Nivel primary key (NI_Clave),
	/*Claves foraneas*/
	constraint fk_Grada foreign key (FK_Grada) references Grada(G_Clave)
);

create table Taquilla_Apuesta(
	TAA_Clave		serial NOT NULL UNIQUE,
	TAA_Numero	numeric(2) NOT NULL,
	FK_Nivel		integer,
	/*Clave primaria*/
	constraint PK_Taquilla_Apuesta primary key (TAA_Clave),
	/*Claves foraneas*/
	constraint fk_Nivel foreign key (FK_Nivel) references Nivel(NI_Clave)
);

create table Usuario(
	U_Clave 							serial not null unique,
	U_Correo_E 						varchar(45) NOT NULL UNIQUE,
	U_Password 						varchar(16) NOT NULL,
	U_Fecha_Registro 			date not null,
	FK_Entrenador 				Numeric(10),
	FK_Propietario 				Numeric(10),
	FK_Jinete 						Numeric(10),
	FK_Veterinario 				Numeric(10),
	FK_Aficionado 				Numeric(10),
	FK_Tipo_Usuario 			integer not null,
	/*Clave primaria*/
	constraint PK_Usuario 		primary key(U_Clave),
	/*Claves foraneas*/
	constraint FK_Entrenador 		foreign key(FK_Entrenador) references Entrenador(P_Cedula),
	constraint FK_Propietario 	foreign key(FK_Propietario) references Propietario(P_Cedula),
	constraint FK_Jinete 				foreign key(FK_Jinete) references Jinete(P_Cedula),
	constraint FK_Veterinario 	foreign key(FK_Veterinario) references Veterinario(P_Cedula),
	constraint FK_Aficionado 		foreign key(FK_Aficionado) references Aficionado(P_Cedula),
	constraint FK_Tipo_Usuario 	foreign key(FK_Tipo_Usuario) references Tipo_Usuario(TU_Clave)
);

create table Taquilla_Boleto(
	TAB_Clave		serial NOT NULL UNIQUE,
	TAB_Numero	numeric(2) NOT NULL,
	FK_Nivel 		integer	NOT NULL,
	/*Clave primaria*/
	constraint PK_Taquilla_Boleto primary key (TAB_Clave),
	/*Claves foraneas*/
	constraint fk_Nivel foreign key (FK_Nivel) references Nivel(NI_Clave)
);

create table Venta_Boleto(
	VB_Clave				    serial NOT NULL UNIQUE,
	VB_Fecha				    date NOT NULL,
	VB_Total_Venta			numeric(10,2) NOT NULL,
	FK_Taquilla_Boleto	integer,
	FK_Usuario					integer,
	FK_Aficionado				integer,
	/*Clave primaria*/
	constraint PK_Venta_Boleto primary key (VB_Clave),
	/*Claves foraneas*/
	constraint fk_Taquilla_Boleto foreign key (FK_Taquilla_Boleto) references Taquilla_Boleto(TAB_Clave),
	constraint fk_Usuario foreign key (FK_Usuario) references Usuario(U_Clave),
	constraint fk_Aficionado foreign key (FK_Aficionado) references Aficionado(P_Cedula)
);

create table Boleto(
	BO_Clave 		serial NOT NULL UNIQUE,
	BO_Precio 	numeric(10,2) NOT NULL,
	FK_Nivel		integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Boleto primary key (BO_Clave),
	/*Claves foraneas*/
	constraint fk_Nivel foreign key (FK_Nivel) references Nivel(NI_Clave)
);

create table Detallado_Venta(
	DV_Clave					serial NOT NULL UNIQUE,
	DV_Precio_Venta		numeric(10,2) NOT NULL,
	FK_Venta_Boleto		integer NOT NULL,
	FK_Boleto					integer NOT NULL,
	FK_MetodoPago			integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Detallado_Venta primary key (DV_Clave),
	/*Claves foraneas*/
	constraint fk_Venta_Boleto	foreign key (FK_Venta_Boleto) references Venta_Boleto(VB_Clave),
	constraint fk_Boleto 				foreign key (FK_Boleto) references Boleto(BO_Clave),
	constraint fK_MetodoPago	 	foreign key (FK_MetodoPago) references Metodo_Pago(MP_Clave)
);

create table Restaurant(
	R_Rif							numeric(10) NOT NULL UNIQUE,
	R_Razon_Social		varchar(45) NOT NULL,
	R_Capacidad 			numeric(10) NOT NULL,
	FK_Nivel					integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Restaurant primary key (R_Rif),
	/*Claves foraneas*/
	constraint fk_Nivel foreign key (FK_Nivel) references Nivel(NI_Clave)
);

create table Horario(
	HO_Clave				serial NOT NULL UNIQUE,
	HO_Dia_Semana			varchar(9) NOT NULL,
	HO_Hora_Apertura		time NOT NULL,
	HO_Hora_Cierre			time NOT NULL,
	FK_Hipodromo			integer,
	/*Checks*/
	constraint Check_Dia_Semana_Horario CHECK (HO_Dia_Semana in ('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO')),
	/*Clave primaria*/
	constraint PK_Horario primary key (HO_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Pista(
	PI_Clave				serial NOT NULL UNIQUE,
	PI_Longitud			numeric(5)	NOT NULL,
	PI_Capacidad		numeric(3) NOT NULL,
	PI_Num_Salida 	numeric(10) NOT NULL,
	PI_Tipo					varchar(45) NOT NULL,
	FK_Hipodromo		integer,
	/*Checks*/
	constraint Check_Pista_Longitud CHECK (PI_Longitud=1800),
	constraint Check_Pista_Capacidad CHECK (PI_Capacidad=16),
	constraint Check_Pista_Num_Salida CHECK (PI_Num_Salida=2),
	constraint Check_Pista_Tipo CHECK (PI_Tipo in ('ARENA', 'GRAVA')),
	/*Clave primaria*/
	constraint PK_Pista primary key (PI_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Paddock(
	PA_Clave 						serial NOT NULL UNIQUE,
	PA_Numero_Puestos		numeric(10) NOT NULL,
	FK_Hipodromo				integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Paddock primary key (PA_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Circulo_Ganadores(
	CG_Clave									serial NOT NULL UNIQUE,
	CG_CapacidadEjemplares		numeric(10) NOT NULL,
	FK_Hipodromo							integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Circulo_Ganadores primary key (CG_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Historico_Entrenador(
	HE_Clave					serial NOT NULL UNIQUE,
	HE_Fecha_Inicio		date NOT NULL,
	HE_Fecha_Fin			date,
	HE_Activo					boolean NOT NULL,
	FK_Caballeriza		integer NOT NULL,
	FK_Entrenador			numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Historico_Entrenador primary key (HE_Clave),
	/*Claves foraneas*/
	constraint fk_Caballeriza foreign key (FK_Caballeriza) references Caballeriza(CA_Clave),
	constraint fk_Entrenador foreign key (FK_Entrenador) references Entrenador(P_Cedula)
);

create table Venta_Restaurant(
	VR_Clave					serial NOT NULL UNIQUE,
	VR_Fecha_Hora			timestamp NOT NULL,
	VR_Monto_Total		numeric(10) NOT NULL,
	FK_Restaurant			integer NOT NULL,

	/*Clave primaria*/
	constraint PK_Venta_Restaurant primary key (VR_Clave),
	/*Claves foraneas*/
	constraint fk_Restaurant foreign key (FK_Restaurant) references Restaurant(R_Rif)
);

create table Propietario_Stud(
	PS_Clave 				serial NOT NULL UNIQUE,
	PS_Porcentaje		numeric(10) NOT NULL,
	FK_Stud 				integer NOT NULL,
	FK_Propietario	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Propietario_Stud primary key (PS_Clave),
	/*Claves foraneas*/
	constraint fk_Stud foreign key (FK_Stud) references Stud(S_Clave),
	constraint fk_Propietario foreign key (FK_Propietario) references Propietario(P_Cedula)
);

create table Ejemplar_Propietario_Stud(
	EPS_Clave							serial NOT NULL UNIQUE,
	EPS_Porcentaje				numeric(10) NOT NULL,
	FK_Ejemplar						numeric(10) NOT NULL,
	FK_Propietario_Stud		integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Ejemplar_Propietario_Stud primary key (EPS_Clave),
	/*Claves foraneas*/
	constraint fk_Ejemplar foreign key (FK_Ejemplar) references Ejemplar(E_Tatuaje_Labial),
	constraint fk_Propietario_Stud foreign key (FK_Propietario_Stud) references Propietario_Stud(PS_Clave)
);

create table Stud_Color(
	SC_Clave				serial NOT NULL UNIQUE,
	SC_Chaquetilla	boolean NOT NULL,
	SC_Gorra				boolean NOT NULL,
	FK_Color				integer NOT NULL,
	FK_Stud					integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Stud_Color primary key (SC_Clave),
	/*Claves foraneas*/
	constraint fk_Color foreign key (FK_Color) references Color(COL_Clave),
	constraint fk_Stud foreign key (FK_Stud) references Stud(S_Clave)
);

create	table Medicamento(
	M_Codigo						serial NOT NULL UNIQUE,
	M_Nombre						varchar(20) NOT NULL,
	M_Descripcion				varchar(45),
	FK_Tipo_Medicamento	integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Medicamento primary key(M_Codigo),
	/*Clave foranea*/
	constraint fk_Tipo_Medicamento foreign key (FK_Tipo_Medicamento) references Tipo_Medicamento(TM_Clave)
);

create	table Carrera(
	C_Clave								serial NOT NULL UNIQUE,
	C_Nombre							varchar(45) ,
	C_Fecha								date NOT NULL,
	C_Hora								time NOT NULL,
	C_Num_Llamado					Numeric(10) NOT NULL,
	C_Pull_Dinero_Total		Numeric(10),
	C_Distancia						Numeric(10) NOT NULL,
	C_Comentario					varchar(100),
	FK_Tipo_Carrera				integer NOT NULL,
	FK_Categoria_Carrera	integer NOT NULL,
	FK_Pista							integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Carrera primary key(C_Clave),
	/*Claves foraneas*/
	constraint fk_Tipo_Carrera foreign key (FK_Tipo_Carrera) references Tipo_Carrera(TC_Clave),
	constraint fk_Categoria_Carrera foreign key (FK_Categoria_Carrera) references Categoria_Carrera(CA_Clave),
	constraint fK_Pista foreign key (FK_Pista) references Pista(PI_Clave)
);

create	table Carrera_Porcentaje_Dividendo(
	CPD_Clave									serial NOT NULL UNIQUE,
	CPD_Monto_Otorgar					decimal		NOT NULL,
	FK_Carrera								integer NOT NULL,
	FK_Porcentaje_Dividendo		integer NOT NULL,
	/*Clave primaria*/
	constraint PK_Carrera_Percentaje_Dividendo  primary key (CPD_Clave),
	/*Claves foraneas*/
	constraint fk_Carrera foreign key (FK_Carrera) references Carrera(C_Clave),
	constraint fk_Porcentaje_Dividendo foreign key (FK_Porcentaje_Dividendo) references Porcentaje_Dividendo(PD_Clave)
);

create table Inscripcion(
	INS_Clave								serial not null unique ,
	INS_Num_Gualdrapa				Numeric(20) not null,
	INS_Puesto_Pista				Numeric(20) not null,
	INS_Fecha								date  not null,
	INS_Ejemplar_Favorito		boolean,
	INS_Precio_Reclamado		Decimal,
	FK_Carrera							integer not null,
	FK_Binomio							integer not null,
	FK_Implemento						integer not null,
	/*Clave primaria*/
	constraint PK_Inscripcion primary key(INS_Clave),
	/*Clave foranea*/
	constraint FK_Carrera foreign key(FK_Carrera) references Carrera(C_Clave),
	constraint FK_Binomio foreign key(FK_Binomio) references Binomio(BI_Clave),
	constraint FK_Implemento foreign key(FK_Implemento) references Implemento(I_Codigo)
	
);

create table Aplicacion_Medicamento(
	AM_Clave						serial not null unique ,
	AM_Fecha_Hora				timestamp not null,
	FK_Inscripcion			integer not null,
	/*Clave primaria*/
	constraint PK_Aplicacion_Medicamento primary key(AM_Clave),
	/*Clave foranea*/
	constraint FK_Inscripcion foreign key(FK_Inscripcion) references Inscripcion(INS_Clave)
);

 create table Comentario(
	COM_Clave						serial not null unique ,
	COM_Descripcion			Varchar(45) not null,
	FK_Usuario					integer not null,
	FK_Inscripcion			integer not null,
	/*Clave primaria*/
	constraint PK_Comentario primary key(COM_Clave	),
	/*Clave foranea*/
	constraint FK_Usuario foreign key(FK_Usuario) references Usuario(U_Clave),
	constraint FK_Inscripcion foreign key(FK_Inscripcion) references Inscripcion(INS_Clave)
	
);

create table Retiro(
	R_Clave							serial not null unique ,
	R_Fecha_Retiro			Date not null, 
	R_Descripcion				Varchar(45) not null,
	FK_CausaRetiro			integer not null,
	FK_Inscripcion			integer not null,
	/*Clave primaria*/
	constraint PK_Retiro primary key(R_Clave),
	/*Clave foranea*/
	constraint FK_Causa_Retiro foreign key(FK_CausaRetiro) references Causa_Retiro(CR_Clave)
);

create table Resultado_Ejemplar(
	RES_Clave								serial not null unique ,
	RES_Orden_Llegada				Numeric(10) not null, 
	RES_Diferencia_Cuerpos	Numeric(10) not null,
	RES_Dividendo_Pagado		Decimal not null,
	RES_Speed_Rating				Numeric(20) not null, 
	RES_Variante_Pista			Numeric(20) not null,
	FK_Inscripcion					integer not null,
	/*Clave primaria*/
	constraint PK_Resultado_Ejemplar primary key(RES_Clave),
	/*Clave foranea*/
	constraint FK_Inscripcion foreign key(FK_Inscripcion) references Inscripcion(INS_Clave)
);

create table Posicion_Parcial(
	PP_Clave								serial not null unique ,
	PP_Distancia						Numeric(10) not null, 
	PP_Tiempo								Time not null,
	PP_Posicion							Numeric(10) not null,  
	FK_Resultado_Ejemplar		integer not null,
	/*Clave primaria*/
	constraint PK_Posicion_Parcial primary key(PP_Clave),
	/*Clave foranea*/
	constraint FK_Resultado_Ejemplar foreign key(FK_Resultado_Ejemplar) references Resultado_Ejemplar(RES_Clave)
	
);

create table Solicitud_Implemento(
	SI_Clave						serial not null unique ,
	SI_Fecha_Solicitud	Date not null, 
	SI_Aceptada					char(1) not null,
	FK_Implemento  			integer not null,
	FK_Inscripcion			integer not null,
	FK_Usuario					integer not null,
	/*Clave primaria*/
	constraint PK_Solicitud_Implemento primary key(SI_Clave),
	/*Clave foranea*/
	constraint FK_Implemento foreign key(FK_Implemento) references Implemento(I_Codigo),
	constraint FK_Inscripcion foreign key(FK_Inscripcion) references Inscripcion(INS_Clave),
	constraint FK_Usuario foreign key(FK_Usuario) references Usuario(U_Clave),
	/*Checks*/
	constraint Check_SI_Aceptada check (SI_Aceptada in('S','N'))
);


create table Telefono(
	T_ID							serial not null unique ,
	T_Codigo_Area			varchar(4) not null, 
	T_Numero					varchar(7) not null,
	T_Prefijo					varchar(3) not null,
	T_Tipo						varchar(45) not null,  
	FK_Hipodromo 			integer,
	FK_Propietario		Numeric(10),
	/*Clave primaria*/
	constraint PK_Telefono primary key(T_ID),
	/*Clave foranea*/
	constraint FK_Hipodromo  foreign key(FK_Hipodromo ) references Hipodromo(H_ID),
	constraint FK_Propietario foreign key(FK_Propietario) references Propietario(P_Cedula),

	/*Checks*/
	constraint Check_Tipo_Telefono check (T_Tipo in('Local','Trabajo','Movil'))
);

create table Accion_Usuario(
	AU_Clave										serial not null unique,
	AU_Fecha_Hora								timestamp not null unique,
	AU_Clave_Elemento_Afectado	Numeric(10) not null,
	FK_Usuario									integer not null,
	FK_Accion										integer not null,
	/*Clave primaria*/
	constraint PK_Accion_Usuario	primary key(AU_Clave),
	/*Claves foraneas*/
	constraint FK_Usuario		foreign key(FK_Usuario) references Usuario(U_Clave),
	constraint FK_Accion		foreign key(FK_Accion) references Accion(ACC_Clave)
);

create table Accion_Tipo_Usuario(
	ATU_Clave				serial not null unique,
	FK_TipoUsuario	integer not null,
	FK_Accion				integer not null,
	/*Clave primaria*/
	constraint PK_Accion_Tipo_Usuario primary key(ATU_Clave),
	/*Claves foraneas*/
	constraint FK_Tipo_Usuario foreign key(FK_TipoUsuario) references Tipo_Usuario(TU_Clave),
	constraint FK_Accion foreign key(FK_Accion) references Accion(ACC_Clave)
);

create Table Apuesta(
	APU_Clave						serial  not null unique,
	APU_Saldo_Total			Decimal(10,2) not null,
	APU_Combinacion			Numeric(5),
	APU_Fecha_Hora			timestamp not null,
	FK_TipoApuesta			integer not null,
	FK_Usuario					integer,
	FK_Aficionado				Numeric(10),
	/*Clave primaria*/
	constraint PK_Apuesta 		primary key(APU_Clave),
	/*Claves foraneas*/
	constraint FK_TipoApuesta 	foreign key(FK_TipoApuesta) references Tipo_Apuesta(TA_Clave),
	constraint FK_Usuario 		foreign key(FK_Usuario) references Usuario(U_Clave),
	constraint FK_Aficionado	foreign key(FK_Aficionado) references Aficionado(P_Cedula)
);

create table Detalle_Apuesta(
	DA_Clave										serial not null unique ,
	DA_Orden_Llegada_Ejemplar		Numeric(2) not null,
	FK_Apuesta									integer not null,
	FK_Inscripcion						  integer not null,
	FK_MetodoPago								integer NOT NULL,
	/*Clave primaria*/	
	constraint PK_Detalle_Apuesta	primary key(DA_Clave),
	/*Claves foraneas*/
	constraint FK_Apuesta 			foreign key(FK_Apuesta) references Apuesta(APU_Clave),
	constraint FK_Inscripcion 	foreign key(FK_Inscripcion) references Inscripcion(INS_Clave),
	constraint fK_MetodoPago	 	foreign key(FK_MetodoPago) references Metodo_Pago(MP_Clave)

);

create table Restaurant_Horario(
	RH_Clave 				serial not null unique,
	FK_Horario			integer not null,
	FK_Restaurant		numeric(10) not null,
	/*Clave primaria*/	
	constraint PK_Restaurant_Horario	primary key(RH_Clave),
	/*Claves foraneas*/
	constraint fK_Horario 		foreign key(FK_Horario) references Horario(HO_Clave),
	constraint fK_Restaurant	foreign key(FK_Restaurant) references Restaurant(R_Rif)
);

create table Historico_Puesto(
	HP_Clave				serial not null unique,
	HP_Fecha_Inicio date not null,
	HP_Fecha_Final 	date,
	FK_Puesto 			integer not null,
	FK_Ejemplar 		numeric(10) not null,
	/*Clave primaria*/	
	constraint PK_Historico_Puesto	primary key(HP_Clave),
	/*Claves foraneas*/
	constraint fK_Puesto 		foreign key(FK_Puesto) references Puesto(PU_Clave),
	constraint fK_Ejemplar	foreign key(FK_Ejemplar) references Ejemplar(E_Tatuaje_Labial)
);
