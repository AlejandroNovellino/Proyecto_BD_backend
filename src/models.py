# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
# errors imports
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class Accion(db.Model):
    __tablename__ = 'accion'

    acc_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    acc_nombre = db.Column(db.String(45), nullable=False)
    acc_tabla_objetivo = db.Column(db.String(45), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class AccionTipoUsuario(db.Model):
    __tablename__ = 'accion_tipo_usuario'

    atu_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    fk_tipousuario = db.Column(db.ForeignKey('tipo_usuario.tu_clave'), nullable=False)
    fk_accion = db.Column(db.ForeignKey('accion.acc_clave'), nullable=False)

    accion = db.relationship('Accion', primaryjoin='AccionTipoUsuario.fk_accion == Accion.acc_clave', backref='accion_tipo_usuarios')
    tipo_usuario = db.relationship('TipoUsuario', primaryjoin='AccionTipoUsuario.fk_tipousuario == TipoUsuario.tu_clave', backref='accion_tipo_usuarios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class AccionUsuario(db.Model):
    __tablename__ = 'accion_usuario'

    au_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    au_fecha_hora = db.Column(db.DateTime, nullable=False, unique=True)
    au_clave_elemento_afectado = db.Column(db.Numeric(10, 0), nullable=False)
    fk_usuario = db.Column(db.ForeignKey('usuario.u_clave'), nullable=False)
    fk_accion = db.Column(db.ForeignKey('accion.acc_clave'), nullable=False)

    accion = db.relationship('Accion', primaryjoin='AccionUsuario.fk_accion == Accion.acc_clave', backref='accion_usuarios')
    usuario = db.relationship('Usuario', primaryjoin='AccionUsuario.fk_usuario == Usuario.u_clave', backref='accion_usuarios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Aficionado(db.Model):
    __tablename__ = 'aficionado'
    __table_args__ = (
        db.CheckConstraint("p_sexo = ANY (ARRAY['M'::bpchar, 'F'::bpchar])"),
    )

    p_cedula = db.Column(db.Numeric(10, 0), primary_key=True)
    p_primer_nombre = db.Column(db.String(20), nullable=False)
    p_segundo_nombre = db.Column(db.String(20))
    p_primer_apellido = db.Column(db.String(20), nullable=False)
    p_segundo_apellido = db.Column(db.String(20))
    p_sexo = db.Column(db.String(1), nullable=False)
    p_direccion = db.Column(db.String(50), nullable=False)
    af_profesion = db.Column(db.String(30))
    fk_lugar = db.Column(db.ForeignKey('lugar.l_clave'), nullable=False)

    lugar = db.relationship('Lugar', primaryjoin='Aficionado.fk_lugar == Lugar.l_clave', backref='aficionados')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class AplicacionMedicamento(db.Model):
    __tablename__ = 'aplicacion_medicamento'

    am_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    am_fecha_hora = db.Column(db.DateTime, nullable=False)
    fk_inscripcion = db.Column(db.ForeignKey('inscripcion.ins_clave'), nullable=False)

    inscripcion = db.relationship('Inscripcion', primaryjoin='AplicacionMedicamento.fk_inscripcion == Inscripcion.ins_clave', backref='aplicacion_medicamentoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Apuesta(db.Model):
    __tablename__ = 'apuesta'

    apu_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    apu_saldo_total = db.Column(db.Numeric(10, 2), nullable=False)
    apu_combinacion = db.Column(db.Numeric(5, 0))
    apu_fecha_hora = db.Column(db.DateTime, nullable=False)
    fk_tipoapuesta = db.Column(db.ForeignKey('tipo_apuesta.ta_clave'), nullable=False)
    fk_usuario = db.Column(db.ForeignKey('usuario.u_clave'))
    fk_aficionado = db.Column(db.ForeignKey('aficionado.p_cedula'))

    aficionado = db.relationship('Aficionado', primaryjoin='Apuesta.fk_aficionado == Aficionado.p_cedula', backref='apuestas')
    tipo_apuesta = db.relationship('TipoApuesta', primaryjoin='Apuesta.fk_tipoapuesta == TipoApuesta.ta_clave', backref='apuestas')
    usuario = db.relationship('Usuario', primaryjoin='Apuesta.fk_usuario == Usuario.u_clave', backref='apuestas')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Binomio(db.Model):
    __tablename__ = 'binomio'

    bi_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    fk_ejemplar = db.Column(db.ForeignKey('ejemplar.e_tatuaje_labial'), nullable=False)
    fk_jinete = db.Column(db.ForeignKey('jinete.p_cedula'), nullable=False)
    bi_jinete_peso = db.Column(db.Numeric(10, 0), nullable=False)
    bi_ejemplar_peso = db.Column(db.Numeric(10, 0), nullable=False)

    ejemplar = db.relationship('Ejemplar', primaryjoin='Binomio.fk_ejemplar == Ejemplar.e_tatuaje_labial', backref='binomios')
    jinete = db.relationship('Jinete', primaryjoin='Binomio.fk_jinete == Jinete.p_cedula', backref='binomios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Boleto(db.Model):
    __tablename__ = 'boleto'

    bo_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    bo_precio = db.Column(db.Numeric(10, 2), nullable=False)
    fk_nivel = db.Column(db.ForeignKey('nivel.ni_clave'), nullable=False)

    nivel = db.relationship('Nivel', primaryjoin='Boleto.fk_nivel == Nivel.ni_clave', backref='boletoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Caballeriza(db.Model):
    __tablename__ = 'caballeriza'

    ca_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    ca_numero = db.Column(db.Numeric(10, 0), nullable=False)
    ca_capacidad = db.Column(db.Numeric(10, 0), nullable=False)
    fk_hipodromo = db.Column(db.ForeignKey('hipodromo.h_id'), nullable=False)

    hipodromo = db.relationship('Hipodromo', primaryjoin='Caballeriza.fk_hipodromo == Hipodromo.h_id', backref='caballerizas')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Carrera(db.Model):
    __tablename__ = 'carrera'

    c_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    c_nombre = db.Column(db.String(45))
    c_fecha = db.Column(db.Date, nullable=False)
    c_hora = db.Column(db.Time, nullable=False)
    c_num_llamado = db.Column(db.Numeric(10, 0), nullable=False)
    c_pull_dinero_total = db.Column(db.Numeric(10, 0))
    c_distancia = db.Column(db.Numeric(10, 0), nullable=False)
    c_comentario = db.Column(db.String(100))
    fk_tipo_carrera = db.Column(db.ForeignKey('tipo_carrera.tc_clave'), nullable=False)
    fk_categoria_carrera = db.Column(db.ForeignKey('categoria_carrera.ca_clave'), nullable=False)
    fk_pista = db.Column(db.ForeignKey('pista.pi_clave'), nullable=False)

    categoria_carrera = db.relationship('CategoriaCarrera', primaryjoin='Carrera.fk_categoria_carrera == CategoriaCarrera.ca_clave', backref='carreras')
    pista = db.relationship('Pista', primaryjoin='Carrera.fk_pista == Pista.pi_clave', backref='carreras')
    tipo_carrera = db.relationship('TipoCarrera', primaryjoin='Carrera.fk_tipo_carrera == TipoCarrera.tc_clave', backref='carreras')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception as e:
            print(e)
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class CarreraPorcentajeDividendo(db.Model):
    __tablename__ = 'carrera_porcentaje_dividendo'

    cpd_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    cpd_monto_otorgar = db.Column(db.Numeric, nullable=False)
    fk_carrera = db.Column(db.ForeignKey('carrera.c_clave'), nullable=False)
    fk_porcentaje_dividendo = db.Column(db.ForeignKey('porcentaje_dividendo.pd_clave'), nullable=False)

    carrera = db.relationship('Carrera', primaryjoin='CarreraPorcentajeDividendo.fk_carrera == Carrera.c_clave', backref='carrera_porcentaje_dividendoes')
    porcentaje_dividendo = db.relationship('PorcentajeDividendo', primaryjoin='CarreraPorcentajeDividendo.fk_porcentaje_dividendo == PorcentajeDividendo.pd_clave', backref='carrera_porcentaje_dividendoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class CategoriaCarrera(db.Model):
    __tablename__ = 'categoria_carrera'
    __table_args__ = (
        db.CheckConstraint("(ca_nombre)::text = ANY ((ARRAY['Normal'::character varying, 'Clasico'::character varying, 'Copa'::character varying])::text[])"),
    )

    ca_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    ca_nombre = db.Column(db.String(20), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class CausaRetiro(db.Model):
    __tablename__ = 'causa_retiro'

    cr_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    cr_descripcion = db.Column(db.String(45), nullable=False)
    cr_nombre = db.Column(db.String(45), nullable=False)
    cr_duracion = db.Column(db.Numeric(10, 0), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class CirculoGanadore(db.Model):
    __tablename__ = 'circulo_ganadores'

    cg_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    cg_capacidadejemplares = db.Column(db.Numeric(10, 0), nullable=False)
    fk_hipodromo = db.Column(db.ForeignKey('hipodromo.h_id'), nullable=False)

    hipodromo = db.relationship('Hipodromo', primaryjoin='CirculoGanadore.fk_hipodromo == Hipodromo.h_id', backref='circulo_ganadores')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Color(db.Model):
    __tablename__ = 'color'

    col_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    col_nombre = db.Column(db.String(45), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Comentario(db.Model):
    __tablename__ = 'comentario'

    com_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    com_descripcion = db.Column(db.String(45), nullable=False)
    fk_usuario = db.Column(db.ForeignKey('usuario.u_clave'), nullable=False)
    fk_inscripcion = db.Column(db.ForeignKey('inscripcion.ins_clave'), nullable=False)

    inscripcion = db.relationship('Inscripcion', primaryjoin='Comentario.fk_inscripcion == Inscripcion.ins_clave', backref='comentarios')
    usuario = db.relationship('Usuario', primaryjoin='Comentario.fk_usuario == Usuario.u_clave', backref='comentarios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class DetalladoVenta(db.Model):
    __tablename__ = 'detallado_venta'

    dv_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    dv_precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    fk_venta_boleto = db.Column(db.ForeignKey('venta_boleto.vb_clave'), nullable=False)
    fk_boleto = db.Column(db.ForeignKey('boleto.bo_clave'), nullable=False)
    fk_metodopago = db.Column(db.ForeignKey('metodo_pago.mp_clave'), nullable=False)

    boleto = db.relationship('Boleto', primaryjoin='DetalladoVenta.fk_boleto == Boleto.bo_clave', backref='detallado_ventas')
    metodo_pago = db.relationship('MetodoPago', primaryjoin='DetalladoVenta.fk_metodopago == MetodoPago.mp_clave', backref='detallado_ventas')
    venta_boleto = db.relationship('VentaBoleto', primaryjoin='DetalladoVenta.fk_venta_boleto == VentaBoleto.vb_clave', backref='detallado_ventas')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class DetalleApuesta(db.Model):
    __tablename__ = 'detalle_apuesta'

    da_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    da_orden_llegada_ejemplar = db.Column(db.Numeric(2, 0), nullable=False)
    fk_apuesta = db.Column(db.ForeignKey('apuesta.apu_clave'), nullable=False)
    fk_inscripcion = db.Column(db.ForeignKey('inscripcion.ins_clave'), nullable=False)
    fk_metodopago = db.Column(db.ForeignKey('metodo_pago.mp_clave'), nullable=False)

    apuesta = db.relationship('Apuesta', primaryjoin='DetalleApuesta.fk_apuesta == Apuesta.apu_clave', backref='detalle_apuestas')
    inscripcion = db.relationship('Inscripcion', primaryjoin='DetalleApuesta.fk_inscripcion == Inscripcion.ins_clave', backref='detalle_apuestas')
    metodo_pago = db.relationship('MetodoPago', primaryjoin='DetalleApuesta.fk_metodopago == MetodoPago.mp_clave', backref='detalle_apuestas')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Ejemplar(db.Model):
    __tablename__ = 'ejemplar'
    __table_args__ = (
        db.CheckConstraint("(e_color_pelaje)::text = ANY ((ARRAY['C'::character varying, 'Z'::character varying, 'T'::character varying, 'A'::character varying])::text[])"),
        db.CheckConstraint("(e_sexo)::text = ANY ((ARRAY['Y'::character varying, 'C'::character varying])::text[])")
    )

    e_tatuaje_labial = db.Column(db.Numeric(10, 0), primary_key=True)
    e_nombre = db.Column(db.String(45), nullable=False)
    e_color_pelaje = db.Column(db.String(45), nullable=False)
    e_sexo = db.Column(db.String(10), nullable=False)
    e_fecha_nacimiento = db.Column(db.Date, nullable=False)
    e_fecha_ing_hipo = db.Column(db.Date, nullable=False)
    e_peso = db.Column(db.Numeric(5, 0), nullable=False)
    fk_haras = db.Column(db.ForeignKey('haras.h_clave'), nullable=False)
    fk_madre = db.Column(db.ForeignKey('ejemplar.e_tatuaje_labial'))
    fk_padre = db.Column(db.ForeignKey('ejemplar.e_tatuaje_labial'))
    fk_puesto = db.Column(db.ForeignKey('puesto.pu_clave'), nullable=False)
    fk_caballeriza = db.Column(db.ForeignKey('caballeriza.ca_clave'), nullable=False)

    caballeriza = db.relationship('Caballeriza', primaryjoin='Ejemplar.fk_caballeriza == Caballeriza.ca_clave', backref='ejemplars')
    hara = db.relationship('Hara', primaryjoin='Ejemplar.fk_haras == Hara.h_clave', backref='ejemplars')
    parent = db.relationship('Ejemplar', remote_side=[e_tatuaje_labial], primaryjoin='Ejemplar.fk_madre == Ejemplar.e_tatuaje_labial', backref='ejemplar_ejemplars')
    parent1 = db.relationship('Ejemplar', remote_side=[e_tatuaje_labial], primaryjoin='Ejemplar.fk_padre == Ejemplar.e_tatuaje_labial', backref='ejemplar_ejemplars_0')
    puesto = db.relationship('Puesto', primaryjoin='Ejemplar.fk_puesto == Puesto.pu_clave', backref='ejemplars')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class EjemplarPropietarioStud(db.Model):
    __tablename__ = 'ejemplar_propietario_stud'

    eps_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    eps_porcentaje = db.Column(db.Numeric(10, 0), nullable=False)
    fk_ejemplar = db.Column(db.ForeignKey('ejemplar.e_tatuaje_labial'), nullable=False)
    fk_propietario_stud = db.Column(db.ForeignKey('propietario_stud.ps_clave'), nullable=False)

    ejemplar = db.relationship('Ejemplar', primaryjoin='EjemplarPropietarioStud.fk_ejemplar == Ejemplar.e_tatuaje_labial', backref='ejemplar_propietario_studs')
    propietario_stud = db.relationship('PropietarioStud', primaryjoin='EjemplarPropietarioStud.fk_propietario_stud == PropietarioStud.ps_clave', backref='ejemplar_propietario_studs')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Entrada(db.Model):
    __tablename__ = 'entrada'

    en_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    en_letra_identificacion = db.Column(db.String(1), nullable=False)
    en_zona = db.Column(db.String(45), nullable=False)
    fk_grada = db.Column(db.ForeignKey('grada.g_clave'), nullable=False)

    grada = db.relationship('Grada', primaryjoin='Entrada.fk_grada == Grada.g_clave', backref='entradas')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Entrenador(db.Model):
    __tablename__ = 'entrenador'
    __table_args__ = (
        db.CheckConstraint("p_sexo = ANY (ARRAY['M'::bpchar, 'F'::bpchar])"),
    )

    p_cedula = db.Column(db.Numeric(10, 0), primary_key=True)
    p_primer_nombre = db.Column(db.String(20), nullable=False)
    p_segundo_nombre = db.Column(db.String(20))
    p_primer_apellido = db.Column(db.String(20), nullable=False)
    p_segundo_apellido = db.Column(db.String(20))
    p_sexo = db.Column(db.String(1), nullable=False)
    p_direccion = db.Column(db.String(50), nullable=False)
    ent_fecha_ing_hipo = db.Column(db.Date, nullable=False)
    fk_lugar = db.Column(db.ForeignKey('lugar.l_clave'), nullable=False)

    lugar = db.relationship('Lugar', primaryjoin='Entrenador.fk_lugar == Lugar.l_clave', backref='entrenadors')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Estacionamiento(db.Model):
    __tablename__ = 'estacionamiento'

    e_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    e_capacidad_total = db.Column(db.Numeric(4, 0), nullable=False)
    fk_entrada = db.Column(db.ForeignKey('entrada.en_clave'), nullable=False)

    entrada = db.relationship('Entrada', primaryjoin='Estacionamiento.fk_entrada == Entrada.en_clave', backref='estacionamientoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Grada(db.Model):
    __tablename__ = 'grada'

    g_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    g_nombre = db.Column(db.String(45), nullable=False)
    g_capacidad = db.Column(db.Numeric(5, 0), nullable=False)
    fk_hipodromo = db.Column(db.ForeignKey('hipodromo.h_id'), nullable=False)

    hipodromo = db.relationship('Hipodromo', primaryjoin='Grada.fk_hipodromo == Hipodromo.h_id', backref='gradas')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Hara(db.Model):
    __tablename__ = 'haras'

    h_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    h_nombre = db.Column(db.String(45), nullable=False)
    fk_lugar = db.Column(db.ForeignKey('lugar.l_clave'), nullable=False)

    lugar = db.relationship('Lugar', primaryjoin='Hara.fk_lugar == Lugar.l_clave', backref='haras')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Hipodromo(db.Model):
    __tablename__ = 'hipodromo'

    h_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    h_nombre = db.Column(db.String(45), nullable=False, unique=True)
    h_direccion = db.Column(db.String(100), nullable=False, unique=True)
    h_fecha_creacion = db.Column(db.Date, nullable=False)
    h_descripcion_historica = db.Column(db.Text, nullable=False, unique=True)
    fk_lugar = db.Column(db.ForeignKey('lugar.l_clave'), nullable=False)

    lugar = db.relationship('Lugar', primaryjoin='Hipodromo.fk_lugar == Lugar.l_clave', backref='hipodromoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class HistoricoEntrenador(db.Model):
    __tablename__ = 'historico_entrenador'

    he_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    he_fecha_inicio = db.Column(db.Date, nullable=False)
    he_fecha_fin = db.Column(db.Date)
    he_activo = db.Column(db.Boolean, nullable=False)
    fk_caballeriza = db.Column(db.ForeignKey('caballeriza.ca_clave'), nullable=False)
    fk_entrenador = db.Column(db.ForeignKey('entrenador.p_cedula'), nullable=False)

    caballeriza = db.relationship('Caballeriza', primaryjoin='HistoricoEntrenador.fk_caballeriza == Caballeriza.ca_clave', backref='historico_entrenadors')
    entrenador = db.relationship('Entrenador', primaryjoin='HistoricoEntrenador.fk_entrenador == Entrenador.p_cedula', backref='historico_entrenadors')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception as e:
            db.session.rollback()
            print(e)
            raise Exception("A problem ocurred")
        return element

class HistoricoPuesto(db.Model):
    __tablename__ = 'historico_puesto'

    hp_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    hp_fecha_inicio = db.Column(db.Date, nullable=False)
    hp_fecha_final = db.Column(db.Date)
    fk_puesto = db.Column(db.ForeignKey('puesto.pu_clave'), nullable=False)
    fk_ejemplar = db.Column(db.ForeignKey('ejemplar.e_tatuaje_labial'), nullable=False)

    ejemplar = db.relationship('Ejemplar', primaryjoin='HistoricoPuesto.fk_ejemplar == Ejemplar.e_tatuaje_labial', backref='historico_puestoes')
    puesto = db.relationship('Puesto', primaryjoin='HistoricoPuesto.fk_puesto == Puesto.pu_clave', backref='historico_puestoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Horario(db.Model):
    __tablename__ = 'horario'
    __table_args__ = (
        db.CheckConstraint("(ho_dia_semana)::text = ANY ((ARRAY['LUNES'::character varying, 'MARTES'::character varying, 'MIERCOLES'::character varying, 'JUEVES'::character varying, 'VIERNES'::character varying, 'SABADO'::character varying, 'DOMINGO'::character varying])::text[])"),
    )

    ho_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    ho_dia_semana = db.Column(db.String(9), nullable=False)
    ho_hora_apertura = db.Column(db.Time, nullable=False)
    ho_hora_cierre = db.Column(db.Time, nullable=False)
    fk_hipodromo = db.Column(db.ForeignKey('hipodromo.h_id'))

    hipodromo = db.relationship('Hipodromo', primaryjoin='Horario.fk_hipodromo == Hipodromo.h_id', backref='horarios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Implemento(db.Model):
    __tablename__ = 'implemento'
    __table_args__ = (
        db.CheckConstraint("(i_diminutivo)::text = ANY ((ARRAY['GR'::character varying, 'CC'::character varying, 'CH'::character varying, 'LA'::character varying, 'BZ'::character varying, 'BL'::character varying, 'BB'::character varying, 'M'::character varying, 'P'::character varying, 'G'::character varying, 'V'::character varying, 'OT'::character varying, 'L'::character varying])::text[])"),
        db.CheckConstraint("(i_nombre)::text = ANY ((ARRAY['Gringola'::character varying, 'Lengua Amarrada'::character varying, 'Bozal'::character varying, 'Bozal Lenguero'::character varying, 'Bozal Blanco Nose Band'::character varying, 'Martingala'::character varying, 'Preta'::character varying, 'Guayo'::character varying, 'Vendas'::character varying, 'Orejas Tapadas'::character varying, 'Latigo'::character varying, 'Casquillos Correctivos'::character varying, 'Casquillos de Hierro'::character varying])::text[])")
    )

    i_codigo = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    i_nombre = db.Column(db.String(45), nullable=False)
    i_diminutivo = db.Column(db.String(3), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Inscripcion(db.Model):
    __tablename__ = 'inscripcion'

    ins_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    ins_num_gualdrapa = db.Column(db.Numeric(20, 0), nullable=False)
    ins_puesto_pista = db.Column(db.Numeric(20, 0), nullable=False)
    ins_fecha = db.Column(db.Date, nullable=False)
    ins_ejemplar_favorito = db.Column(db.Boolean)
    ins_precio_reclamado = db.Column(db.Numeric)
    fk_carrera = db.Column(db.ForeignKey('carrera.c_clave'), nullable=False)
    fk_binomio = db.Column(db.ForeignKey('binomio.bi_clave'), nullable=False)
    fk_implemento = db.Column(db.ForeignKey('implemento.i_codigo'), nullable=False)

    binomio = db.relationship('Binomio', primaryjoin='Inscripcion.fk_binomio == Binomio.bi_clave', backref='inscripcions')
    carrera = db.relationship('Carrera', primaryjoin='Inscripcion.fk_carrera == Carrera.c_clave', backref='inscripcions')
    implemento = db.relationship('Implemento', primaryjoin='Inscripcion.fk_implemento == Implemento.i_codigo', backref='inscripcions')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Jinete(db.Model):
    __tablename__ = 'jinete'
    __table_args__ = (
        db.CheckConstraint("(j_rango)::text = ANY ((ARRAY['APRENDIZ'::character varying, 'PROFESIONAL'::character varying])::text[])"),
        db.CheckConstraint("p_sexo = ANY (ARRAY['M'::bpchar, 'F'::bpchar])")
    )

    p_cedula = db.Column(db.Numeric(10, 0), primary_key=True)
    p_primer_nombre = db.Column(db.String(20), nullable=False)
    p_segundo_nombre = db.Column(db.String(20))
    p_primer_apellido = db.Column(db.String(20), nullable=False)
    p_segundo_apellido = db.Column(db.String(20))
    p_sexo = db.Column(db.String(1), nullable=False)
    p_direccion = db.Column(db.String(50), nullable=False)
    j_altura = db.Column(db.Numeric(3, 2), nullable=False)
    j_peso_al_ingresar = db.Column(db.Numeric(2, 0), nullable=False)
    j_peso_actual = db.Column(db.Numeric(2, 0), nullable=False)
    j_rango = db.Column(db.String(15))
    j_fecha_nacimiento = db.Column(db.Date, nullable=False)
    fk_lugar = db.Column(db.ForeignKey('lugar.l_clave'), nullable=False)

    lugar = db.relationship('Lugar', primaryjoin='Jinete.fk_lugar == Lugar.l_clave', backref='jinetes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Lugar(db.Model):
    __tablename__ = 'lugar'
    __table_args__ = (
        db.CheckConstraint("(l_tipo)::text = ANY ((ARRAY['Estado'::character varying, 'Municipio'::character varying, 'Parroquia'::character varying])::text[])"),
    )

    l_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    l_nombre = db.Column(db.String(45), nullable=False)
    l_tipo = db.Column(db.String(45), nullable=False)
    fk_lugar = db.Column(db.ForeignKey('lugar.l_clave'))

    parent = db.relationship('Lugar', remote_side=[l_clave], primaryjoin='Lugar.fk_lugar == Lugar.l_clave', backref='lugars')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Medicamento(db.Model):
    __tablename__ = 'medicamento'

    m_codigo = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    m_nombre = db.Column(db.String(20), nullable=False)
    m_descripcion = db.Column(db.String(45))
    fk_tipo_medicamento = db.Column(db.ForeignKey('tipo_medicamento.tm_clave'), nullable=False)

    tipo_medicamento = db.relationship('TipoMedicamento', primaryjoin='Medicamento.fk_tipo_medicamento == TipoMedicamento.tm_clave', backref='medicamentoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class MetodoPago(db.Model):
    __tablename__ = 'metodo_pago'

    mp_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    mp_nombre = db.Column(db.String(56))

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Nivel(db.Model):
    __tablename__ = 'nivel'

    ni_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    ni_apartado_4p = db.Column(db.Numeric(3, 0), nullable=False)
    ni_apartado_6p = db.Column(db.Numeric(3, 0), nullable=False)
    ni_apartado_8p = db.Column(db.Numeric(3, 0), nullable=False)
    fk_grada = db.Column(db.ForeignKey('grada.g_clave'), nullable=False)

    grada = db.relationship('Grada', primaryjoin='Nivel.fk_grada == Grada.g_clave', backref='nivels')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Paddock(db.Model):
    __tablename__ = 'paddock'

    pa_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    pa_numero_puestos = db.Column(db.Numeric(10, 0), nullable=False)
    fk_hipodromo = db.Column(db.ForeignKey('hipodromo.h_id'), nullable=False)

    hipodromo = db.relationship('Hipodromo', primaryjoin='Paddock.fk_hipodromo == Hipodromo.h_id', backref='paddocks')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Pista(db.Model):
    __tablename__ = 'pista'
    __table_args__ = (
        db.CheckConstraint("(pi_tipo)::text = ANY ((ARRAY['ARENA'::character varying, 'GRAVA'::character varying])::text[])"),
        db.CheckConstraint('pi_capacidad = (16)::numeric'),
        db.CheckConstraint('pi_longitud = (1800)::numeric'),
        db.CheckConstraint('pi_num_salida = (2)::numeric')
    )

    pi_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    pi_longitud = db.Column(db.Numeric(5, 0), nullable=False)
    pi_capacidad = db.Column(db.Numeric(3, 0), nullable=False)
    pi_num_salida = db.Column(db.Numeric(10, 0), nullable=False)
    pi_tipo = db.Column(db.String(45), nullable=False)
    fk_hipodromo = db.Column(db.ForeignKey('hipodromo.h_id'))

    hipodromo = db.relationship('Hipodromo', primaryjoin='Pista.fk_hipodromo == Hipodromo.h_id', backref='pistas')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class PorcentajeDividendo(db.Model):
    __tablename__ = 'porcentaje_dividendo'

    pd_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    pd_puesto = db.Column(db.Numeric(3, 0), nullable=False)
    pd_porcentaje = db.Column(db.Numeric(3, 2), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class PosicionParcial(db.Model):
    __tablename__ = 'posicion_parcial'

    pp_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    pp_distancia = db.Column(db.Numeric(10, 0), nullable=False)
    pp_tiempo = db.Column(db.Time, nullable=False)
    pp_posicion = db.Column(db.Numeric(10, 0), nullable=False)
    fk_resultado_ejemplar = db.Column(db.ForeignKey('resultado_ejemplar.res_clave'), nullable=False)

    resultado_ejemplar = db.relationship('ResultadoEjemplar', primaryjoin='PosicionParcial.fk_resultado_ejemplar == ResultadoEjemplar.res_clave', backref='posicion_parcials')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Propietario(db.Model):
    __tablename__ = 'propietario'
    __table_args__ = (
        db.CheckConstraint("p_sexo = ANY (ARRAY['M'::bpchar, 'F'::bpchar])"),
    )

    p_cedula = db.Column(db.Numeric(10, 0), primary_key=True)
    p_primer_nombre = db.Column(db.String(20), nullable=False)
    p_segundo_nombre = db.Column(db.String(20))
    p_primer_apellido = db.Column(db.String(20), nullable=False)
    p_segundo_apellido = db.Column(db.String(20))
    p_sexo = db.Column(db.String(1), nullable=False)
    p_direccion = db.Column(db.String(50), nullable=False)
    pr_correo = db.Column(db.String(40), nullable=False, unique=True)
    pr_fecha_nacimiento = db.Column(db.Date, nullable=False)
    fk_lugar = db.Column(db.ForeignKey('lugar.l_clave'), nullable=False)

    lugar = db.relationship('Lugar', primaryjoin='Propietario.fk_lugar == Lugar.l_clave', backref='propietarios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class PropietarioStud(db.Model):
    __tablename__ = 'propietario_stud'

    ps_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    ps_porcentaje = db.Column(db.Numeric(10, 0), nullable=False)
    fk_stud = db.Column(db.ForeignKey('stud.s_clave', ondelete='CASCADE'), nullable=False)
    fk_propietario = db.Column(db.ForeignKey('propietario.p_cedula', ondelete='CASCADE'), nullable=False)

    propietario = db.relationship('Propietario', primaryjoin='PropietarioStud.fk_propietario == Propietario.p_cedula', backref='propietario_studs')
    stud = db.relationship('Stud', primaryjoin='PropietarioStud.fk_stud == Stud.s_clave', backref='propietario_studs')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Puesto(db.Model):
    __tablename__ = 'puesto'
    __table_args__ = (
        db.CheckConstraint('(pu_numero >= (1)::numeric) AND (pu_numero <= (50)::numeric)'),
    )

    pu_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    pu_numero = db.Column(db.Numeric(10, 0), nullable=False)
    fk_caballeriza = db.Column(db.ForeignKey('caballeriza.ca_clave'), nullable=False)

    caballeriza = db.relationship('Caballeriza', primaryjoin='Puesto.fk_caballeriza == Caballeriza.ca_clave', backref='puestoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    r_rif = db.Column(db.Numeric(10, 0), primary_key=True)
    r_razon_social = db.Column(db.String(45), nullable=False)
    r_capacidad = db.Column(db.Numeric(10, 0), nullable=False)
    fk_nivel = db.Column(db.ForeignKey('nivel.ni_clave'), nullable=False)

    nivel = db.relationship('Nivel', primaryjoin='Restaurant.fk_nivel == Nivel.ni_clave', backref='restaurants')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class RestaurantHorario(db.Model):
    __tablename__ = 'restaurant_horario'

    rh_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    fk_horario = db.Column(db.ForeignKey('horario.ho_clave'), nullable=False)
    fk_restaurant = db.Column(db.ForeignKey('restaurant.r_rif'), nullable=False)

    horario = db.relationship('Horario', primaryjoin='RestaurantHorario.fk_horario == Horario.ho_clave', backref='restaurant_horarios')
    restaurant = db.relationship('Restaurant', primaryjoin='RestaurantHorario.fk_restaurant == Restaurant.r_rif', backref='restaurant_horarios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class ResultadoEjemplar(db.Model):
    __tablename__ = 'resultado_ejemplar'

    res_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    res_orden_llegada = db.Column(db.Numeric(10, 0), nullable=False)
    res_diferencia_cuerpos = db.Column(db.Numeric(10, 0), nullable=False)
    res_dividendo_pagado = db.Column(db.Numeric, nullable=False)
    res_speed_rating = db.Column(db.Numeric(20, 0), nullable=False)
    res_variante_pista = db.Column(db.Numeric(20, 0), nullable=False)
    fk_inscripcion = db.Column(db.ForeignKey('inscripcion.ins_clave'), nullable=False)

    inscripcion = db.relationship('Inscripcion', primaryjoin='ResultadoEjemplar.fk_inscripcion == Inscripcion.ins_clave', backref='resultado_ejemplars')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Retiro(db.Model):
    __tablename__ = 'retiro'

    r_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    r_fecha_retiro = db.Column(db.Date, nullable=False)
    r_descripcion = db.Column(db.String(45), nullable=False)
    fk_causaretiro = db.Column(db.ForeignKey('causa_retiro.cr_clave'), nullable=False)
    fk_inscripcion = db.Column(db.ForeignKey('inscripcion.ins_clave'), nullable=False)

    causa_retiro = db.relationship('CausaRetiro', primaryjoin='Retiro.fk_causaretiro == CausaRetiro.cr_clave', backref='retiros')
    inscripcion = db.relationship('Inscripcion', primaryjoin='Retiro.fk_inscripcion == Inscripcion.ins_clave', backref='retiros')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class SolicitudImplemento(db.Model):
    __tablename__ = 'solicitud_implemento'
    __table_args__ = (
        db.CheckConstraint("si_aceptada = ANY (ARRAY['S'::bpchar, 'N'::bpchar])"),
    )

    si_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    si_fecha_solicitud = db.Column(db.Date, nullable=False)
    si_aceptada = db.Column(db.String(1), nullable=False)
    fk_implemento = db.Column(db.ForeignKey('implemento.i_codigo'), nullable=False)
    fk_inscripcion = db.Column(db.ForeignKey('inscripcion.ins_clave'), nullable=False)
    fk_usuario = db.Column(db.ForeignKey('usuario.u_clave'), nullable=False)

    implemento = db.relationship('Implemento', primaryjoin='SolicitudImplemento.fk_implemento == Implemento.i_codigo', backref='solicitud_implementoes')
    inscripcion = db.relationship('Inscripcion', primaryjoin='SolicitudImplemento.fk_inscripcion == Inscripcion.ins_clave', backref='solicitud_implementoes')
    usuario = db.relationship('Usuario', primaryjoin='SolicitudImplemento.fk_usuario == Usuario.u_clave', backref='solicitud_implementoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Stud(db.Model):
    __tablename__ = 'stud'

    s_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    s_nombre = db.Column(db.String(45), nullable=False)
    s_fecha_creacion = db.Column(db.Date, nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class StudColor(db.Model):
    __tablename__ = 'stud_color'

    sc_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    sc_chaquetilla = db.Column(db.Boolean, nullable=False)
    sc_gorra = db.Column(db.Boolean, nullable=False)
    fk_color = db.Column(db.ForeignKey('color.col_clave', ondelete='CASCADE'), nullable=False)
    fk_stud = db.Column(db.ForeignKey('stud.s_clave', ondelete='CASCADE'), nullable=False)

    color = db.relationship('Color', primaryjoin='StudColor.fk_color == Color.col_clave', backref='stud_colors')
    stud = db.relationship('Stud', primaryjoin='StudColor.fk_stud == Stud.s_clave', backref='stud_colors')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception as e:
            print(e)
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class TaquillaApuesta(db.Model):
    __tablename__ = 'taquilla_apuesta'

    taa_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    taa_numero = db.Column(db.Numeric(2, 0), nullable=False)
    fk_nivel = db.Column(db.ForeignKey('nivel.ni_clave'))

    nivel = db.relationship('Nivel', primaryjoin='TaquillaApuesta.fk_nivel == Nivel.ni_clave', backref='taquilla_apuestas')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class TaquillaBoleto(db.Model):
    __tablename__ = 'taquilla_boleto'

    tab_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    tab_numero = db.Column(db.Numeric(2, 0), nullable=False)
    fk_nivel = db.Column(db.ForeignKey('nivel.ni_clave'), nullable=False)

    nivel = db.relationship('Nivel', primaryjoin='TaquillaBoleto.fk_nivel == Nivel.ni_clave', backref='taquilla_boletoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Telefono(db.Model):
    __tablename__ = 'telefono'
    __table_args__ = (
        db.CheckConstraint("(t_tipo)::text = ANY ((ARRAY['Local'::character varying, 'Trabajo'::character varying, 'Movil'::character varying])::text[])"),
    )

    t_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    t_codigo_area = db.Column(db.String(4), nullable=False)
    t_numero = db.Column(db.String(7), nullable=False)
    t_prefijo = db.Column(db.String(3), nullable=False)
    t_tipo = db.Column(db.String(45), nullable=False)
    fk_hipodromo = db.Column(db.ForeignKey('hipodromo.h_id'))
    fk_propietario = db.Column(db.ForeignKey('propietario.p_cedula'))

    hipodromo = db.relationship('Hipodromo', primaryjoin='Telefono.fk_hipodromo == Hipodromo.h_id', backref='telefonoes')
    propietario = db.relationship('Propietario', primaryjoin='Telefono.fk_propietario == Propietario.p_cedula', backref='telefonoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class TipoApuesta(db.Model):
    __tablename__ = 'tipo_apuesta'

    ta_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    ta_nombre = db.Column(db.String(20), nullable=False)
    ta_precio = db.Column(db.Numeric(6, 2), nullable=False)
    ta_saldo_minimo = db.Column(db.Numeric(6, 2))
    ta_precio_jugada_adicional = db.Column(db.Numeric(10, 2))
    ta_cant_caballo_minimo_carrera = db.Column(db.Numeric(3, 0))
    ta_num_ejemplar_minimo_necesario = db.Column(db.Numeric(3, 0))

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class TipoCarrera(db.Model):
    __tablename__ = 'tipo_carrera'
    __table_args__ = (
        db.CheckConstraint("(tc_sexo)::text = ANY ((ARRAY['Y'::character varying, 'C'::character varying])::text[])"),
    )

    tc_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    tc_nombre = db.Column(db.String(60), nullable=False)
    tc_sexo = db.Column(db.String(1))
    tc_edad_minima = db.Column(db.Numeric(4, 0))
    tc_edad_maxima = db.Column(db.Numeric(4, 0))
    tc_victoria_minima = db.Column(db.Numeric(4, 0))
    tc_victoria_maxima = db.Column(db.Numeric(4, 0))

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class TipoMedicamento(db.Model):
    __tablename__ = 'tipo_medicamento'

    tm_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    tm_nombre = db.Column(db.String(20), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'

    tu_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    tu_nombre = db.Column(db.String(45), nullable=False)

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Usuario(db.Model):
    __tablename__ = 'usuario'

    u_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    u_correo_e = db.Column(db.String(45), nullable=False, unique=True)
    u_password = db.Column(db.String(16), nullable=False)
    u_fecha_registro = db.Column(db.Date, nullable=False)
    fk_entrenador = db.Column(db.ForeignKey('entrenador.p_cedula'))
    fk_propietario = db.Column(db.ForeignKey('propietario.p_cedula'))
    fk_jinete = db.Column(db.ForeignKey('jinete.p_cedula'))
    fk_veterinario = db.Column(db.ForeignKey('veterinario.p_cedula'))
    fk_aficionado = db.Column(db.ForeignKey('aficionado.p_cedula'))
    fk_tipo_usuario = db.Column(db.ForeignKey('tipo_usuario.tu_clave'), nullable=False)

    aficionado = db.relationship('Aficionado', primaryjoin='Usuario.fk_aficionado == Aficionado.p_cedula', backref='usuarios')
    entrenador = db.relationship('Entrenador', primaryjoin='Usuario.fk_entrenador == Entrenador.p_cedula', backref='usuarios')
    jinete = db.relationship('Jinete', primaryjoin='Usuario.fk_jinete == Jinete.p_cedula', backref='usuarios')
    propietario = db.relationship('Propietario', primaryjoin='Usuario.fk_propietario == Propietario.p_cedula', backref='usuarios')
    tipo_usuario = db.relationship('TipoUsuario', primaryjoin='Usuario.fk_tipo_usuario == TipoUsuario.tu_clave', backref='usuarios')
    veterinario = db.relationship('Veterinario', primaryjoin='Usuario.fk_veterinario == Veterinario.p_cedula', backref='usuarios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class VentaBoleto(db.Model):
    __tablename__ = 'venta_boleto'

    vb_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    vb_fecha = db.Column(db.Date, nullable=False)
    vb_total_venta = db.Column(db.Numeric(10, 2), nullable=False)
    fk_taquilla_boleto = db.Column(db.ForeignKey('taquilla_boleto.tab_clave'))
    fk_usuario = db.Column(db.ForeignKey('usuario.u_clave'))
    fk_aficionado = db.Column(db.ForeignKey('aficionado.p_cedula'))

    aficionado = db.relationship('Aficionado', primaryjoin='VentaBoleto.fk_aficionado == Aficionado.p_cedula', backref='venta_boletoes')
    taquilla_boleto = db.relationship('TaquillaBoleto', primaryjoin='VentaBoleto.fk_taquilla_boleto == TaquillaBoleto.tab_clave', backref='venta_boletoes')
    usuario = db.relationship('Usuario', primaryjoin='VentaBoleto.fk_usuario == Usuario.u_clave', backref='venta_boletoes')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class VentaRestaurant(db.Model):
    __tablename__ = 'venta_restaurant'

    vr_clave = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    vr_fecha_hora = db.Column(db.DateTime, nullable=False)
    vr_monto_total = db.Column(db.Numeric(10, 0), nullable=False)
    fk_restaurant = db.Column(db.ForeignKey('restaurant.r_rif'), nullable=False)

    restaurant = db.relationship('Restaurant', primaryjoin='VentaRestaurant.fk_restaurant == Restaurant.r_rif', backref='venta_restaurants')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element

class Veterinario(db.Model):
    __tablename__ = 'veterinario'
    __table_args__ = (
        db.CheckConstraint("p_sexo = ANY (ARRAY['M'::bpchar, 'F'::bpchar])"),
    )

    p_cedula = db.Column(db.Numeric(10, 0), primary_key=True)
    p_primer_nombre = db.Column(db.String(20), nullable=False)
    p_segundo_nombre = db.Column(db.String(20))
    p_primer_apellido = db.Column(db.String(20), nullable=False)
    p_segundo_apellido = db.Column(db.String(20))
    p_sexo = db.Column(db.String(1), nullable=False)
    p_direccion = db.Column(db.String(50), nullable=False)
    v_numero_colegiatura = db.Column(db.Numeric(10, 0), nullable=False)
    fk_lugar = db.Column(db.ForeignKey('lugar.l_clave'), nullable=False)
    fk_caballeriza = db.Column(db.ForeignKey('caballeriza.ca_clave'), nullable=False)

    caballeriza = db.relationship('Caballeriza', primaryjoin='Veterinario.fk_caballeriza == Caballeriza.ca_clave', backref='veterinarios')
    lugar = db.relationship('Lugar', primaryjoin='Veterinario.fk_lugar == Lugar.l_clave', backref='veterinarios')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Key not unique")
        except Exception:
            db.session.rollback()
            raise Exception("A problem ocurred")
        return element
