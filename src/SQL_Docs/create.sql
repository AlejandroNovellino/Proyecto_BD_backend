create	table Tipo_Medicamento(
	TM_Clave	numeric(10) NOT NULL UNIQUE,
	TM_Nombre	varchar(20) NOT NULL,
	constraint PK_tipoMedicamento primary key(TM_Clave)

);

create	table Medicamento(
	M_Codigo			numeric(10) NOT NULL UNIQUE,
	M_Nombre			varchar(20) NOT NULL,
	M_Descripcion		varchar(45),
	FK_Tipo_Medicamento	numeric(10) NOT NULL,
	constraint PK_Medicamento primary key(M_Codigo),
	constraint fk_Tipo_Medicamento foreign key (FK_Tipo_Medicamento) references Tipo_Medicamento(TM_Clave)

);

create	table Categoria_Carrera(
	CA_Clave			numeric(10) NOT NULL UNIQUE,
	CA_Nombre			varchar(20) NOT NULL,
	
	constraint PK_Categoria_Carrera primary key(CA_Clave),
	constraint Check_Categoria_Nombre Check (CA_Nombre IN ('Normal','Clasico','Copa')) 
);

create	table Tipo_Carrera(
	TC_Clave				numeric(10) NOT NULL UNIQUE,
	TC_Nombre				varchar(20) NOT NULL,
	TC_Sexo					varchar(45),
	TC_Edad_Minima			Numeric(10),
	TC_Edad_Maxima			Numeric(10),
	TC_Victoria_Minima		Numeric(10),
	TC_Victoria_Maxima		Numeric(10),
	constraint PK_Tipo_Carrera primary key(TC_Clave),
	constraint Check_Categoria_Genero Check (TC_Sexo IN ('Y','C')) 
);

create	table Carrera(
	C_Clave				numeric(10) NOT NULL UNIQUE,
	C_Nombre				varchar(45) ,
	C_Fecha					date NOT NULL,
	C_Hora					time NOT NULL,
	C_Num_Llamado			Numeric(10) NOT NULL,
	C_Pull_Dinero_Total		Numeric(10),
	C_Distancia				Numeric(10) NOT NULL,
	C_Comentario			varchar(100),
	FK_Tipo_Carrera			numeric(10) NOT NULL,
	FK_Categoria_Carrera	numeric(10) NOT NULL,
	constraint PK_Carrera primary key(C_Clave),
	constraint fk_Tipo_Carrera foreign key (FK_Tipo_Carrera) references Tipo_Carrera(TC_Clave),
	constraint fk_Categoria_Carrera foreign key (FK_Categoria_Carrera) references Categoria_Carrera(CA_Clave)
);

create	table Porcentaje_Dividendo(
	PD_Clave			numeric(10) NOT NULL UNIQUE,
	PD_Puesto			numeric(3) NOT NULL,
	PD_Porcentaje		varchar(45)	NOT NULL,
	constraint PK_Porcentaje_Dividendo primary key(PD_Clave)
	
);
create	table Carrera_Porcentaje_Dividendo(
	CPD_Clave				numeric(10) NOT NULL UNIQUE,
	CPD_Monto_Otorgar		decimal		NOT NULL,
	FK_Carrera				numeric(10) NOT NULL,
	FK_Porcentaje_Dividendo	numeric(10) NOT NULL,
	constraint PK_Carrera_Percentaje_Dividendo  primary key (CPD_Clave),
	constraint fk_Carrera foreign key (FK_Carrera) references Carrera(C_Clave),
	constraint fk_Porcentaje_Dividendo foreign key (FK_Porcentaje_Dividendo) references Porcentaje_Dividendo(PD_Clave)
);

alter  table Carrera_Porcentaje_Dividendo ADD constraint PK_Carrera_Percentaje_Dividendo  primary key (CPD_Clave);

create	table Causa_Retiro(
	CR_Clave				numeric(10) NOT NULL UNIQUE,
	CR_Descripcion			varchar(45)	NOT NULL,
	CR_Nombre				varchar(45) NOT NULL,
	CR_Duracion				numeric(10) NOT NULL,
	constraint PK_Causa_Retiro  primary key (CR_Clave)
	
);

create table Implemento(
	I_Codigo				numeric(10) NOT NULL UNIQUE,
	I_Nombre				varchar(45)	NOT NULL,
	I_Diminutivo			varchar(3) NOT NULL,
	constraint PK_Implemento  primary key (I_Codigo),
	constraint Check_Implemento_Nombre Check (I_Nombre IN ('Gringola','Lengua ','Amarrada
','Bozal','Bozal Lengüero','Bozal Blanco','Nose Band
','Martingala ','Preta','Guayo','Vendas','Orejas Tapadas','Látigo','Casquillos ','Correctivos','Casquillos de Hierro') ),
	constraint Check_Implemento_Diminutivo Check (I_Diminutivo IN ('CC','CH','LA','BZ','BL','BB','M','P','G','V','OT','L') )
)



