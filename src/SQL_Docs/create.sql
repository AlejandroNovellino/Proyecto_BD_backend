/*Crea la base de datos ---------------------------------------------------------------------------------------*/

create database Proyecto_BD;

/*Paginas de la 2 a la 11---------------------------------------------------------------------------------------*/

	/*Checks*/
	/*Clave primaria*/
	/*Claves foraneas*/

create table Ejemplar(
  E_Tatuaje_Labial    numeric(10) NOT NULL UNIQUE,
  E_Nombre            varchar(45) NOT NULL,
  E_Color_Pelaje      varchar(45) NOT NULL,
  E_Sexo              varchar(10) NOT NULL,
  E_Fecha_Nacimiento  date NOT NULL,
  E_Fecha_Ing_Hipo    date NOT NULL,
  E_Peso              numeric(5) NOT NULL,
  FK_Haras            numeric(10) NOT NULL,
  FK_Madre            numeric(10),
  FK_Padre            numeric(10),
  FK_Puesto           numeric(10) NOT NULL,
  FK_Caballeriza      numeric(10) NOT NULL,
  /*Checks*/
  constraint Check_Ejemplar_Color_Pelaje CHECK (E_Color_Pelaje in ('Z', 'T', 'A')),
  constraint Check_Ejemplar_Sexo CHECK (E_Sexo in ('Y', 'C')),
  /*Clave primaria*/
  constraint PK_Ejemplar primary key (E_Tatuaje_Labial)
  /*Claves foraneas*/
  constraint fk_Haras foreign key (FK_Haras) references Haras(H_Clave),
  constraint fk_Madre foreign key (FK_Madre) references Ejemplar(E_Tatuaje_Labial),
  constraint fk_Padre foreign key (FK_Padre) references Ejemplar(E_Tatuaje_Labial),
  constraint fk_Puesto foreign key (FK_Puesto) references Puesto(PU_Clave),
  constraint fk_Caballeriza foreign key (FK_Caballeriza) references Caballeriza(CA_Clave)
);

create table Binomio(
	BI_Clave 					numeric(10) NOT NULL UNIQUE,
	FK_Ejemplar				numeric(10) NOT NULL,
	FK_Jinete					numeric(10) NOT NULL,
	BI_Jinete_Peso		numeric(10) NOT NULL,
	BI_Ejemplar_Peso 	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint FK_Binomio primary key (BI_Clave),
	/*Claves foraneas*/
	constraint fk_Ejemplar foreign key (FK_Ejemplar) references Ejemplar(E_Tatuaje_Labial),
	constraint fk_Jinete foreign key (FK_Jinete) references Jinete(P_Cedula),
);

create table Haras(
	H_Clave 	numeric(10) NOT NULL UNIQUE,
	H_Nombre 	varchar(45) NOT NULL,
	/*Clave primaria*/
	constraint FK_Haras primary key (H_Clave)
);

create table Lugar(
	L_Clave		numeric(10) NOT NULL UNIQUE,
	L_Nombre 	varchar(45) NOT NULL,
	L_Tipo 		varchar(45) NOT NULL,
	FK_Lugar 	numeric(10),
	/*Checks*/
	constraint Check_Lugar_Tipo CHECK (L_Tipo in ('Pais', 'Estado', 'Parroquia')),
	/*Clave primaria*/
	constraint PK_Lugar primary key (L_Clave),
	/*Claves foraneas*/
	constraint fk_Lugar foreign key (FK_Lugar) references Lugar(FK_Lugar)
);

create table Hipodromo(
	H_ID										numeric(10) NOT NULL UNIQUE,
	H_Nombre 								varchar(45) NOT NULL UNIQUE,
	H_Direccion							varchar(100) NOT NULL UNIQUE,
	H_Fecha_Creacion 				date NOT NULL,
	H_Descripcion_Historica text NOT NULL UNIQUE,
	FK_Lugar 								numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Hipodromo primary key (H_ID),
	/*Claves foraneas*/
	constraint fk_Lugar foreign key (FK_Lugar) references Lugar(L_Clave)
);

create table Grada(
	G_Clave		numeric(10) NOT NULL UNIQUE,
	G_Nombre	varchar(45) NOT NULL,
	G_Capacidad		numeric(10)	NOT NULL,
	FK_Hipodromo	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Grada primary key (G_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Entrada(
	EN_Clave 									numeric(10) NOT NULL UNIQUE;,
	EN_Letra_Identificacion		char(1) NOT NULL,
	EN_Zona 									varchar(45) NOT NULL,
	FK_Grada									numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Entrada primary key (EN_Clave),
	/*Claves foraneas*/
	constraint fk_Grada foreign key (FK_Grada) references Grada(G_Clave)
);

create table Estacionamiento(
	E_Clave							numeric(10) NOT NULL UNIQUE,
	E_Capacidad_Total		numeric(15) NOT NULL,
	FK_Entrada					numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Estacionamiento primary key (E_Clave),
	/*Claves foraneas*/
	constraint fk_Entrada foreign key (FK_Entrada) references Entrada(EN_Clave)
);

create table Nivel(
	NI_Clave				numeric(10) NOT NULL UNIQUE,
	NI_Apartado_4P	numeric(10) NOT NULL,
	NI_Apartado_6P	numeric(10) NOT NULL,
	NI_Apartado_8P	numeric(10) NOT NULL,
	FK_Grada				numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Nivel primary key (NI_Clave)
	/*Claves foraneas*/
	constraint fk_Grada foreign key (FK_Grada) references Grada(G_Clave)
);

create table Taquilla_Apuesta(
	TAA_Clave		numeric(10) NOT NULL UNIQUE,
	TAA_Numero	numeric(10) NOT NULL,
	FK_Nivel		numeric(10),
	/*Clave primaria*/
	constraint PK_Taquilla_Apuesta primary key (TAA_Clave),
	/*Claves foraneas*/
	constraint fk_Nivel foreign key (FK_Nivel) references Nivel(NI_Clave)
);

create table Venta_Boleto(
	VB_Clave						numeric(10) NOT NULL UNIQUE,
	VB_Fecha						date NOT NULL,
	VB_Total_Venta			numeric(10) NOT NULL,
	FK_Taquilla_Boleto	numeric(10),
	FK_Usuario					numeric(10),
	FK_Aficionado				numeric(10),
	/*Clave primaria*/
	constraint PK_Venta_Boleto primary key (VB_Clave),
	/*Claves foraneas*/
	constraint fk_Taquilla_Boleto foreign key (FK_Taquilla_Boleto) references Taquilla_Boleto(TAB_Clave),
	constraint fk_Usuario foreign key (FK_Usuario) references Usuario(U_Clave),
	constraint fk_Aficionado foreign key (FK_Aficionado) references Aficionado(P_Cedula)
);

create table Detallado_Venta(
	DV_Clave					numeric(10) NOT NULL UNIQUE,
	DV_Precio_Venta		numeric(10) NOT NULL,
	FK_Venta_Boleto		numeric(10) NOT NULL,
	FK_Boleto					numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Detallado_Venta primary key (DV_Clave),
	/*Claves foraneas*/
	constraint fk_Venta_Boleto foreign key (FK_Venta_Boleto) references Venta_Boleto(VB_Clave),
	constraint fk_Boleto foreign key (FK_Boleto) references Boleto(BO_Clave)
);

create table Boleto(
	BO_Clave 		numeric(10) NOT NULL UNIQUE,
	BO_Precio 	numeric(10) NOT NULL,
	FK_Nivel		numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Boleto primary key (BO_Clave),
	/*Claves foraneas*/
	constraint fk_Nivel foreign key (FK_Nivel) references Nivel(NI_Clave)
);

create table Taquilla_Boleto(
	TAB_Clave		numeric(10) NOT NULL UNIQUE,
	TAB_Numero	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Taquilla_Boleto primary key (TAB_Clave),
	/*Claves foraneas*/
	constraint fk_Nivel foreign key (FK_Nivel) references Nivel(NI_Clave)
);

create table Caballeriza(
	CA_Clave 			numeric(10) NOT NULL UNIQUE,
	CA_Numero 		numeric(10)	NOT NULL,
	CA_Capacidad	numeric(10) NOT NULL,
	FK_Hipodromo	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Caballeriza primary key (CA_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Horario(
	HO_Clave					numeric(10) NOT NULL UNIQUE,
	HO_Dia_Semana			varchar(45) NOT NULL,
	HO_Hora_Apertura	time NOT NULL,
	HO_Hora_Cierre		time NOT NULL,
	FK_Hipodromo			numeric(10),
	FK_Restaurant			numeric(10),
	/*Checks*/
	constraint Check_Dia_Semana_Horario CHECK (HO_Dia_Semana in ('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO')),
	/*Clave primaria*/
	constraint PK_Horario primary key (HO_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID),
	constraint fk_Restaurant foreign key (FK_Restaurant) references Restaurant(R_Clave)
);

create table Pista(
	PI_Clave			numeric(10) NOT NULL UNIQUE,
	PI_Longitud		numeric(10)	NOT NULL,
	PI_Capacidad	numeric(10) NOT NULL,
	PI_Num_Salida numeric(10) NOT NULL,
	PI_Tipo				varchar(45) NOT NULL,
	FK_Hipodromo	numeric(10)
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
	PA_Clave 					numeric(10) NOT NULL UNIQUE,
	PA_Numero_Puestos	numeric(10) NOT NULL,
	FK_Hipodromo			numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Paddock primary key (PA_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Circulo_Ganadores(
	CG_Clave								numeric(10) NOT NULL UNIQUE,
	CG_CapacidadEjemplares	numeric(10) NOT NULL,
	FK_Hipodromo						numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Circulo_Ganadores primary key (CG_Clave),
	/*Claves foraneas*/
	constraint fk_Hipodromo foreign key (FK_Hipodromo) references Hipodromo(H_ID)
);

create table Puesto(
	PU_Clave				numeric(10) NOT NULL UNIQUE,
	PU_Numero				numeric(10) NOT NULL,
	FK_Caballeriza	numeric(10) NOT NULL,
	/*Checks*/
	constraint Check_Pista_Longitud CHECK (PU_Numero between 1 and 50),
	/*Clave primaria*/
	constraint PK_Puesto primary key (PU_Clave),
	/*Claves foraneas*/
	constraint fk_Caballeriza foreign key (FK_Caballeriza) references Caballeriza(CA_Clave)
);

create table Historico_Entrenador(
	HE_Clave					numeric(10) NOT NULL UNIQUE,
	HE_Fecha_Inicio		date NOT NULL,
	HE_Fecha_Fin			date,
	HE_Activo					boolean NOT NULL,
	FK_Caballeriza		numeric(10) NOT NULL,
	FK_Entrenador			numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Historico_Entrenador primary key (HE_Clave),
	/*Claves foraneas*/
	constraint fk_Caballeriza foreign key (FK_Caballeriza) references Caballeriza(CA_Clave),
	constraint fk_Entrenador foreign key (FK_Entrenador) references Entrenador(P_Cedula)
);

create table Restaurant(
	R_Rif						numeric(10) NOT NULL UNIQUE,
	R_Razon_Social	varchar(45) NOT NULL,
	R_Capacidad 		numeric(10) NOT NULL,
	FK_Nivel				numeric(10) NOT NULL,
	FK_Horario			numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Restaurant primary key (R_Rif),
	/*Claves foraneas*/
	constraint fk_Nivel foreign key (FK_Nivel) references Nivel(NI_Clave),
	constraint fk_Horario foreign key (FK_Horario) references Horario(HO_Clave)
);

create table Venta_Restaurant(
	VR_Clave				numeric(10) NOT NULL UNIQUE,
	VR_Fecha_Hora		timestamp NOT NULL,
	VR_Monto_Total	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Venta_Restaurant primary key (VR_Clave),
	/*Claves foraneas*/
	constraint fk_Restaurant foreign key (FK_Restaurant) references Restaurant(R_Clave)
);

create table Stud(
	S_Clave						numeric(10) NOT NULL UNIQUE,
	S_Nombre					varchar(45) NOT NULL,
	S_Fecha_Creacion	date NOT NULL,
	/*Clave primaria*/
	constraint PK_Stud primary key (S_Clave)
);

create table Propietario_Stud(
	PS_Clave 				numeric(10) NOT NULL UNIQUE,
	PS_Porcentaje		numeric(10) NOT NULL,
	FK_Stud 				numeric(10) NOT NULL,
	FK_Propietario	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Propietario_Stud primary key (PS_Clave)
	/*Claves foraneas*/
	constraint fk_Stud foreign key (FK_Stud) references Stud(S_Clave),
	constraint fk_Propietario foreign key (FK_Propietario) references Propietario(P_Cedula)
);

create table Ejemplar_Propietario_Stud(
	EPS_Clave						numeric(10) NOT NULL UNIQUE,
	EPS_Porcentaje			numeric(10) NOT NULL,
	FK_Ejemplar					numeric(10) NOT NULL,
	FK_Propietario_Stud	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Ejemplar_Propietario_Stud primary key (EPS_Clave)
	/*Claves foraneas*/
	constraint fk_Ejemplar foreign key (FK_Ejemplar) references Ejemplar(E_Tatuaje_Labial),
	constraint fk_Propietario_Stud foreign key (FK_Propietario_Stud) references Propietario_Stud(PS_Clave)
);

create table Stud_Color(
	SC_Clave				numeric(10) NOT NULL UNIQUE,
	SC_Chaquetilla	boolean NOT NULL,
	SC_Gorra				boolean NOT NULL,
	FK_Color				numeric(10) NOT NULL,
	FK_Stud					numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Stud_Color primary key (SC_Clave)
	/*Claves foraneas*/
	constraint fk_Color foreign key (FK_Color) references Color(COL_Clave),
	constraint fk_Stud foreign key (FK_Stud) references Stud(S_Clave)
);

create table Color(
	COL_Clave		numeric(10) NOT NULL,
	COL_Nombre 	varchar(45) NOT NULL,
	/*Clave primaria*/
	constraint PK_Color primary key (COL_Clave)
);

/*Paginas de la 12 a la 20---------------------------------------------------------------------------------------*/

create	table Tipo_Medicamento(
	TM_Clave	numeric(10) NOT NULL UNIQUE,
	TM_Nombre	varchar(20) NOT NULL,
	/*Clave primaria*/
	constraint PK_tipoMedicamento primary key(TM_Clave)

);

create	table Medicamento(
	M_Codigo			numeric(10) NOT NULL UNIQUE,
	M_Nombre			varchar(20) NOT NULL,
	M_Descripcion	varchar(45),
	FK_Tipo_Medicamento	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Medicamento primary key(M_Codigo),
	/*Clave foranea*/
	constraint fk_Tipo_Medicamento foreign key (FK_Tipo_Medicamento) references Tipo_Medicamento(TM_Clave)

);

create	table Categoria_Carrera(
	CA_Clave			numeric(10) NOT NULL UNIQUE,
	CA_Nombre			varchar(20) NOT NULL,
	/*Clave primaria*/
	constraint PK_Categoria_Carrera primary key(CA_Clave),
	/*Clave foranea*/
	constraint Check_Categoria_Nombre Check (CA_Nombre IN ('Normal','Clasico','Copa')) 
);

create	table Tipo_Carrera(
	TC_Clave						numeric(10) NOT NULL UNIQUE,
	TC_Nombre						varchar(20) NOT NULL,
	TC_Sexo							varchar(45),
	TC_Edad_Minima			Numeric(10),
	TC_Edad_Maxima			Numeric(10),
	TC_Victoria_Minima	Numeric(10),
	TC_Victoria_Maxima	Numeric(10),
	/*Clave primaria*/
	constraint PK_Tipo_Carrera primary key(TC_Clave),
	/*Checks*/
	constraint Check_Categoria_Genero Check (TC_Sexo IN ('Y','C')) 
);

create	table Carrera(
	C_Clave								numeric(10) NOT NULL UNIQUE,
	C_Nombre							varchar(45) ,
	C_Fecha								date NOT NULL,
	C_Hora								time NOT NULL,
	C_Num_Llamado					Numeric(10) NOT NULL,
	C_Pull_Dinero_Total		Numeric(10),
	C_Distancia						Numeric(10) NOT NULL,
	C_Comentario					varchar(100),
	FK_Tipo_Carrera				numeric(10) NOT NULL,
	FK_Categoria_Carrera	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Carrera primary key(C_Clave),
	/*Claves foraneas*/
	constraint fk_Tipo_Carrera foreign key (FK_Tipo_Carrera) references Tipo_Carrera(TC_Clave),
	constraint fk_Categoria_Carrera foreign key (FK_Categoria_Carrera) references Categoria_Carrera(CA_Clave)
);

create	table Porcentaje_Dividendo(
	PD_Clave			numeric(10) NOT NULL UNIQUE,
	PD_Puesto			numeric(3) NOT NULL,
	PD_Porcentaje	varchar(45)	NOT NULL,
	/*Clave primaria*/
	constraint PK_Porcentaje_Dividendo primary key(PD_Clave)
);

create	table Carrera_Porcentaje_Dividendo(
	CPD_Clave								numeric(10) NOT NULL UNIQUE,
	CPD_Monto_Otorgar				decimal		NOT NULL,
	FK_Carrera							numeric(10) NOT NULL,
	FK_Porcentaje_Dividendo	numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Carrera_Percentaje_Dividendo  primary key (CPD_Clave),
	/*Claves foraneas*/
	constraint fk_Carrera foreign key (FK_Carrera) references Carrera(C_Clave),
	constraint fk_Porcentaje_Dividendo foreign key (FK_Porcentaje_Dividendo) references Porcentaje_Dividendo(PD_Clave)
);

create	table Causa_Retiro(
	CR_Clave				numeric(10) NOT NULL UNIQUE,
	CR_Descripcion	varchar(45)	NOT NULL,
	CR_Nombre				varchar(45) NOT NULL,
	CR_Duracion			numeric(10) NOT NULL,
	/*Clave primaria*/
	constraint PK_Causa_Retiro  primary key (CR_Clave)
);

create table Implemento(
	I_Codigo				numeric(10) NOT NULL UNIQUE,
	I_Nombre				varchar(45)	NOT NULL,
	I_Diminutivo		varchar(3) NOT NULL,
	/*Clave primaria*/
	constraint PK_Implemento  primary key (I_Codigo),
	/*Checks*/
	constraint Check_Implemento_Nombre Check (I_Nombre IN ('Gringola','Lengua ','Amarrada
		','Bozal','Bozal Lengüero','Bozal Blanco','Nose Band',
		'Martingala ','Preta','Guayo','Vendas','Orejas Tapadas','Látigo','Casquillos ','Correctivos','Casquillos de Hierro') ),
	constraint Check_Implemento_Diminutivo Check (I_Diminutivo IN ('CC','CH','LA','BZ','BL','BB','M','P','G','V','OT','L') )
);

/*Paginas de la 21 en adelante --------------------------------------------------------------------------------------*/

create table Usuario(
	U_Clave 					Numeric(10),
	U_Correo_E 				varchar(45) NOT NULL UNIQUE,
	U_Password 				varchar(16) NOT NULL,
	U_Fecha_Registro 	date not null,
	FK_Entrenador 		Numeric(10),
	FK_Propietario 		Numeric(10),
	FK_Jinete 				Numeric(10),
	FK_Veterinario 		Numeric(10),
	FK_Aficionado 		Numeric(10),
	FK_Tipo_Usuario 	Numeric(10) not null,
	/*Clave primaria*/
	constraint PK_Usuario 		primary key(U_Clave),
	/*Claves foraneas*/
	constraint FK_Entrenador 		foreign key(FK_Entrenador) references Entrenador(P_Cedula),
	constraint FK_Propietario 	foreign key(FK_Propietario) references Propietario(P_Cedula),
	constraint FK_Jinete 				foreign key(FK_Jinete) references Jinete(P_Cedula),
	constraint FK_Veterinario 	foreign key(FK_Veterinario) references Veterinario(P_Cedula),
	constraint FK_Aficionado 		foreign key(FK_Aficionado) references Aficionado(P_Cedula),
	constraint FK_Tipo_Usuario 	foreign key(FK_Tipo-Usuario) references Tipo_Usuario(TU_Clave)
);

create table Accion_Usuario(
	AU_Clave										Numeric(10),
	AU_Fecha_Hora								SmallDateTime not null unique,
	AU_Clave_Elemento_Afectado	Numeric(10) not null,
	FK_Usuario									Numeric(10) not null,
	FK_Accion										Numeric(10) not null,
	/*Clave primaria*/
	constraint PK_Accion_Usuario	primary key(AU_Clave),
	/*Claves foraneas*/
	constraint FK_Usuario		foreign key(FK_Usuario) references Usuario(U_Clave),
	constraint FK_Accion		foreign key(FK_Accion) references Accion(ACC_Clave),
);

create table Accion_Tipo_Usuario(
	ATU_Clave				Numeric(10),
	FK_TipoUsuario	Numeric(10) not null,
	FK_Accion				Numeric(10) not null,
	/*Clave primaria*/
	constraint PK_Accion_Tipo_Usuario primary key(ATU_Clave),
	/*Claves foraneas*/
	constraint FK_Tipo_Usuario foreign key(FK_TipoUsuario) references Tipo_Usuario(TU_Clave),
	constraint FK_Accion foreign key(FK_Accion) references Accion(ACC_Clave),
);

create table Accion(
	ACC_Clave			Numeric(10),
	ACC_Objetivo	Numeric(10) not null unique,
	/*Clave primaria*/
	constraint PK_Accion primary key(ACC_Clave),
);

create table Pregunta_Seguridad(
	PS_Clave		Numeric(10),
	PS_Titulo		Varchar(45) not null,
	/*Clave primaria*/
	constraint PK_Pregunta_Seguridad primary key(PS_Clave),
);

create table Pregunta_Usuario(
	PU_Clave							Numeric(10),
	PU_Respuesta					Varchar(45) not null,
	FK_Usuario						Numeric(10) not null,
	FK_Pregunta_Seguridad	Numeric(10) not null,
	/*Clave primaria*/
	constraint PK_Pregunta_Usuario 	primary key(PU_Clave),
	/*Claves foraneas*/
	constraint FK_Usuario			foreign key(FK_Usuario) references Usuario(U_Clave),
	constraint FK_Pregunta_Seguridad	foreign key(FK_Pregunta_Seguridad) references Pregunta_Seguridad(PS_Clave),
);

create table Tipo_Usuario(
	TU_Clave		Numeric(10),
	TU_Nombre		Varchar(45) not null,
	/*Clave primaria*/
	constraint PK_Tipo_Usuario primary key(TU_Clave),
);

create Table Apuesta(
	APU_Clave				Numeric(10),
	APU_Saldo_Total	Decimal(10,2) not null,
	APU_Combinacion	Numeric(5),
	APU_Fecha_Hora	SmallDateTime not null,
	FK_TipoApuesta	Numeric(10) not null,
	FK_Usuario			Numeric(10),
	FK_Aficionado			Numeric(10),
	/*Clave primaria*/
	constraint PK_Apuesta 		primary key(APU_Clave),
	/*Claves foraneas*/
	constraint FK_TipoApuesta foreign key(FK_TipoApuesta) references Tipo_Apuesta(TA_Clave),
	constraint FK_Usuario 		foreign key(FK_Usuario) references Usuario(U_Clave),
	constraint FK_Aficionado	foreign key(FK_Aficionado) references Aficionado(P_Clave),
);

create Table Tipo_Apuesta(
	TA_Clave													Numeric(10),
	TA_Nombre													Varchar(20) not null,
	TA_Precio													Decimal(6,2) not null,
	TA_Saldo_Minimo										Decimal(6,2),
	TA_Precio_Jugada_Adicional				Numeric(10,2),
	TA_Cant_Caballo_Minimo_Carrera		Numeric(3),
	TA_Num_Ejemplar_Minimo_Necesario	Numeric(3),
	/*Clave primaria*/
	constraint PK_Tipo_Apuesta primary key(TA_Clave),
);

create table Detalle_Apuesta(
	DA_Clave									Numeric(10),
	DA_Orden_Llegada_Ejemplar	Numeric(2) not null,
	FK_Apuesta								Numeric(10) not null,
	FK_Inscripcion						Numeric(10) not null unique,
	/*Clave primaria*/	
	constraint PK_Detalle_Apuesta	primary key(DA_Clave),
	/*Claves foraneas*/
	constraint FK_Apuesta foreign key(FK_Apuesta) references Apuesta(APU_Clave),
	constraint FK_Inscripcion foreign key(FK_Inscripcion) references Inscripcion(INS_Clave),
);	

create table Aficionado(
	P_Cedula						Numeric(10),
	P_Primer_Nombre			Varchar(20) not null,
	P_Segundo_Nombre		Varchar(20),
	P_Primer_Apellido		Varchar(20) not null,
	P_Segundo_Apellido	Varchar(20),
	P_Sexo							Char(1) not null,
	P_Direccion					Varchar(50) not null,
	AF_Profesion				Varchar(30),
	FK_Lugar						Numeric(10) not null,
	/*Clave primaria*/
	constraint PK_Aficionado	primary key(P_Cedula),
	/*Claves foraneas*/
	constraint FK_Lugar 		foreign key(FK_Lugar) references Lugar(L_Clave),
	constraint Check_Sexo check(P_Sexo in('M','F')),
);

create table Entrenador(
	P_Cedula						Numeric(10),
	P_Primer_Nombre			Varchar(20) not null,
	P_Segundo_Nombre		Varchar(20),
	P_Primer_Apellido		Varchar(20) not null,
	P_Segundo_Apellido	Varchar(20),
	P_Sexo							Char(1) not null,
	P_Direccion					Varchar(50) not null,
	ENT_Fecha_Ing_Hipo	Date not null,
	FK_Lugar						Numeric(10) not null,
	/*Clave primaria*/
	constraint PK_Entrenador	primary key(P_Cedula),
	/*Claves foraneas*/
	constraint FK_Lugar foreign key(FK_Lugar) references Lugar(L_Clave),
	constraint Check_Sexo check(P_Sexo in('M','F')),
);

create table Veterinario(
	P_Cedula							Numeric(10),
	P_Primer_Nombre				Varchar(20) not null,
	P_Segundo_Nombre			Varchar(20),
	P_Primer_Apellido			Varchar(20) not null,
	P_Segundo_Apellido		Varchar(20),
	P_Sexo								Char(1) not null,
	P_Direccion						Varchar(50) not null,
	V_Numero_Colegiatura	Numeric(10) not null,
	FK_Lugar							Numeric(10) not null,
	FK_Caballeriza				Numeric(10) not null,
	/*Clave primaria*/
	constraint PK_Veterinario	primary key(P_Cedula),
	/*Claves foraneas*/
	constraint FK_Lugar 		foreign key(FK_Lugar) references Lugar(L_Clave),
	constraint FK_Caballeriza 	foreign key(FK_Caballeriza) references Caballeriza(CA_Clave),
	/*Checks*/
	constraint Check_Sexo check(P_Sexo in('M','F')),
);

create table Propietario(
	P_Cedula						Numeric(10),
	P_Primer_Nombre			Varchar(20) not null,
	P_Segundo_Nombre		Varchar(20),
	P_Primer_Apellido		Varchar(20) not null,
	P_Segundo_Apellido	Varchar(20),
	P_Sexo							Char(1) not null,
	P_Direccion					Varchar(50) not null,
	PR_Correo						Varchar(40) not null unique,
	PR_Fecha_Nacimiento	Date not null,
	FK_Lugar						Numeric(10) not null,
	FK_Telefono					Numeric(10),
	/*Clave primaria*/ 
	constraint PK_Propietario	primary key(P_Cedula),
	/*Claves foraneas*/
	constraint FK_Lugar foreign key(FK_Lugar) references Lugar(L_Clave),
	/*Checks*/
	constraint Check_Sexo check (P_Sexo in('M','F')),
);

create table Jinete(
	P_Cedula						Numeric(10),
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
	FK_Lugar						Numeric(10) not null,
	/*Clave primaria*/
	constraint PK_Jinete primary key(P_Cedula),
	/*Clave foranea*/
	constraint FK_Lugar foreign key(FK_Lugar) references Lugar(L_Clave),
	/*Checks*/
	constraint Check_Sexo 	check(P_Sexo in('M','F')),
	constraint Check_Rango 	check(J_Rango in('Aprendiz','Profesional')), 
);
