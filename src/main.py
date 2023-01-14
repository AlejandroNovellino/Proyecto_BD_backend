"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import datetime
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, generateReport
from admin import setup_admin
from models import *

# marshmellow import
from flask_marshmallow import Marshmallow 
# flask-restful import
from flask_restful import reqparse, abort, Resource, Api, inputs
# simple json module
import simplejson

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# init marshmellow
ma = Marshmallow(app)
# init flask-restful
api = Api(app)

# parsers setup 
# Ejemplar --------------------------------------------------------------------------------
ejemplar_parser = reqparse.RequestParser()
ejemplar_parser.add_argument('e_tatuaje_labial') 
ejemplar_parser.add_argument('e_nombre')
ejemplar_parser.add_argument('e_color_pelaje')
ejemplar_parser.add_argument('e_sexo')
ejemplar_parser.add_argument('e_fecha_nacimiento')
ejemplar_parser.add_argument('e_fecha_ing_hipo')
ejemplar_parser.add_argument('e_peso')
ejemplar_parser.add_argument('fk_haras')
ejemplar_parser.add_argument('fk_madre')
ejemplar_parser.add_argument('fk_padre')
ejemplar_parser.add_argument('fk_puesto')
ejemplar_parser.add_argument('fk_caballeriza')
# Entrenador --------------------------------------------------------------------------------
entrenador_parser = reqparse.RequestParser()
entrenador_parser.add_argument('p_cedula') 
entrenador_parser.add_argument('p_primer_nombre')
entrenador_parser.add_argument('p_segundo_nombre')
entrenador_parser.add_argument('p_primer_apellido')
entrenador_parser.add_argument('p_segundo_apellido')
entrenador_parser.add_argument('p_sexo')
entrenador_parser.add_argument('p_direccion')
entrenador_parser.add_argument('ent_fecha_ing_hipo')
entrenador_parser.add_argument('fk_lugar')
# Jinete --------------------------------------------------------------------------------
jinete_parser = reqparse.RequestParser()
jinete_parser.add_argument('p_cedula') 
jinete_parser.add_argument('p_primer_nombre')
jinete_parser.add_argument('p_segundo_nombre')
jinete_parser.add_argument('p_primer_apellido')
jinete_parser.add_argument('p_segundo_apellido')
jinete_parser.add_argument('p_sexo')
jinete_parser.add_argument('p_direccion')
jinete_parser.add_argument('j_altura')
jinete_parser.add_argument('j_peso_al_ingresar')
jinete_parser.add_argument('j_peso_actual')
jinete_parser.add_argument('j_rango')
jinete_parser.add_argument('j_fecha_nacimiento')
jinete_parser.add_argument('fk_lugar')
# Stud --------------------------------------------------------------------------------
stud_parser = reqparse.RequestParser()
stud_parser.add_argument('s_clave') 
stud_parser.add_argument('s_nombre')
stud_parser.add_argument('s_fecha_creacion')
# Carrera --------------------------------------------------------------------------------
carrera_parser = reqparse.RequestParser()
carrera_parser.add_argument('c_clave') 
carrera_parser.add_argument('c_nombre')
carrera_parser.add_argument('c_fecha')
carrera_parser.add_argument('c_hora')
carrera_parser.add_argument('c_num_llamado')
carrera_parser.add_argument('c_pull_dinero_total')
carrera_parser.add_argument('c_distancia')
carrera_parser.add_argument('c_comentario')
carrera_parser.add_argument('fk_tipo_carrera')
carrera_parser.add_argument('fk_categoria_carrera')
carrera_parser.add_argument('fk_pista')
# Propietario --------------------------------------------------------------------------------
propietario_parser = reqparse.RequestParser()
propietario_parser.add_argument('p_cedula') 
propietario_parser.add_argument('p_primer_nombre')
propietario_parser.add_argument('p_segundo_nombre')
propietario_parser.add_argument('p_primer_apellido')
propietario_parser.add_argument('p_segundo_apellido')
propietario_parser.add_argument('p_sexo')
propietario_parser.add_argument('p_direccion')
propietario_parser.add_argument('pr_correo')
propietario_parser.add_argument('pr_fecha_nacimiento')
propietario_parser.add_argument('fk_lugar')
# Tipo Usuario --------------------------------------------------------------------------------
tipo_usuario_parser = reqparse.RequestParser()
tipo_usuario_parser.add_argument('tu_clave') 
tipo_usuario_parser.add_argument('tu_nombre')
# AccionTipoUsuario --------------------------------------------------------------------------------
accion_tipo_usuario_parser = reqparse.RequestParser()
accion_tipo_usuario_parser.add_argument('atu_clave') 
accion_tipo_usuario_parser.add_argument('fk_tipousuario') 
accion_tipo_usuario_parser.add_argument('fk_accion')
# Usuario --------------------------------------------------------------------------------
usuario_parser = reqparse.RequestParser()
usuario_parser.add_argument('u_clave') 
usuario_parser.add_argument('u_correo_e')
usuario_parser.add_argument('u_password')
usuario_parser.add_argument('u_fecha_registro')
usuario_parser.add_argument('fk_entrenador')
usuario_parser.add_argument('fk_propietario')
usuario_parser.add_argument('fk_jinete')
usuario_parser.add_argument('fk_veterinario')
usuario_parser.add_argument('fk_aficionado')
usuario_parser.add_argument('fk_tipo_usuario')
# AccionUsuario --------------------------------------------------------------------------------
accion_usuario_parser = reqparse.RequestParser()
accion_usuario_parser.add_argument('au_clave') 
accion_usuario_parser.add_argument('au_fecha_hora')
accion_usuario_parser.add_argument('au_clave_elemento_afectado')
accion_usuario_parser.add_argument('fk_usuario')
accion_usuario_parser.add_argument('fk_accion')
# HistoricoEntrenador ----------------------------------------------------------------------------
historico_entrenador_parser = reqparse.RequestParser()
historico_entrenador_parser.add_argument('he_clave') 
historico_entrenador_parser.add_argument('he_fecha_inicio')
historico_entrenador_parser.add_argument('he_fecha_fin')
historico_entrenador_parser.add_argument('he_activo',  type=inputs.boolean)
historico_entrenador_parser.add_argument('fk_caballeriza')
historico_entrenador_parser.add_argument('fk_entrenador')
# PropietarioStud --------------------------------------------------------------------------------
propietario_stud_parser = reqparse.RequestParser()
propietario_stud_parser.add_argument('ps_clave') 
propietario_stud_parser.add_argument('ps_porcentaje')
propietario_stud_parser.add_argument('fk_stud')
propietario_stud_parser.add_argument('fk_propietario')
# StudColor --------------------------------------------------------------------------------------
color_stud_parser = reqparse.RequestParser()
color_stud_parser.add_argument('sc_clave') 
color_stud_parser.add_argument('sc_chaquetilla', type=inputs.boolean)
color_stud_parser.add_argument('sc_gorra', type=inputs.boolean)
color_stud_parser.add_argument('fk_color')
color_stud_parser.add_argument('fk_stud')
# HistoricoPuesto --------------------------------------------------------------------------------
historico_puesto_parser = reqparse.RequestParser()
historico_puesto_parser.add_argument('hp_fecha_inicio') 
historico_puesto_parser.add_argument('hp_fecha_final')
historico_puesto_parser.add_argument('fk_puesto')
historico_puesto_parser.add_argument('fk_ejemplar')
# Binomio --------------------------------------------------------------------------------
binomio_parser = reqparse.RequestParser()
binomio_parser.add_argument('bi_clave') 
binomio_parser.add_argument('fk_ejemplar')
binomio_parser.add_argument('fk_jinete')
binomio_parser.add_argument('bi_jinete_peso')
binomio_parser.add_argument('bi_ejemplar_peso')
# CarreraPorcentajeDividendo --------------------------------------------------------------------------------
cpd_parser = reqparse.RequestParser()
cpd_parser.add_argument('cpd_clave') 
cpd_parser.add_argument('cpd_monto_otorgar')
cpd_parser.add_argument('fk_carrera')
cpd_parser.add_argument('fk_porcentaje_dividendo')
# Inscripcion --------------------------------------------------------------------------------
inscripcion_parser = reqparse.RequestParser()
inscripcion_parser.add_argument('ins_clave') 
inscripcion_parser.add_argument('ins_num_gualdrapa')
inscripcion_parser.add_argument('ins_puesto_pista')
inscripcion_parser.add_argument('ins_fecha')
inscripcion_parser.add_argument('ins_ejemplar_favorito', type=inputs.boolean) 
inscripcion_parser.add_argument('ins_precio_reclamado')
inscripcion_parser.add_argument('fk_carrera')
inscripcion_parser.add_argument('fk_binomio')
inscripcion_parser.add_argument('fk_implemento')
# Retiro --------------------------------------------------------------------------------
retiro_parser = reqparse.RequestParser()
retiro_parser.add_argument('r_clave') 
retiro_parser.add_argument('r_fecha_retiro')
retiro_parser.add_argument('r_descripcion')
retiro_parser.add_argument('fk_causaretiro')
retiro_parser.add_argument('fk_inscripcion') 
# TipoApuesta --------------------------------------------------------------------------------
tipo_apuesta_parser = reqparse.RequestParser()
tipo_apuesta_parser.add_argument('ta_clave') 
tipo_apuesta_parser.add_argument('ta_nombre')
tipo_apuesta_parser.add_argument('ta_precio')
tipo_apuesta_parser.add_argument('ta_saldo_minimo')
tipo_apuesta_parser.add_argument('ta_multiplicador') 
tipo_apuesta_parser.add_argument('ta_precio_jugada_adicional') 
tipo_apuesta_parser.add_argument('ta_cant_minima_caballos_necesaria_en_carrera') 
tipo_apuesta_parser.add_argument('ta_cant_maxima_caballos_por_carrera') 
tipo_apuesta_parser.add_argument('ta_cant_maxima_caballos')
tipo_apuesta_parser.add_argument('ta_cant_valida_ultimas_carreras_programa')
tipo_apuesta_parser.add_argument('ta_llegada_en_orden', type=inputs.boolean)
tipo_apuesta_parser.add_argument('ta_limite_premiado_inferior') 
tipo_apuesta_parser.add_argument('ta_limite_premiado_superior') 
tipo_apuesta_parser.add_argument('ta_descripcion') 
# Color ------------------------------------------------------------------------------------------
color_parser = reqparse.RequestParser()
color_parser.add_argument('col_nombre')
# Report ------------------------------------------------------------------------------------------
report_parser = reqparse.RequestParser()
report_parser.add_argument('file_name')
report_parser.add_argument('db_table')

# schemas for the models -------------------------------------------------------------------------

# Ejemplar schema
class EjemplarSchema(ma.SQLAlchemyAutoSchema):
    #madre
    parent = ma.Nested(lambda: EjemplarSchema(exclude=("parent","parent1",)))
    #padre
    parent1 = ma.Nested(lambda: EjemplarSchema(exclude=("parent","parent1",)))
    class Meta:
        model = Ejemplar
        include_fk = True
        json_module = simplejson
# instance the class
ejemplar_schema = EjemplarSchema()

# Entrenador schema
class EntrenadorSchema(ma.SQLAlchemyAutoSchema):
    #nested schemas
    
    class Meta:
        model = Entrenador
        include_fk = True
        json_module = simplejson
# instance the class
entrenador_schema = EntrenadorSchema()

# Jinete schema
class JineteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Jinete
        include_fk = True
        json_module = simplejson
# instance the class
jinete_schema = JineteSchema()

# Stud schema
class StudSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stud
        include_fk = True
# instance the class
stud_schema = StudSchema()

# Propietario schema
class PropietarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Propietario
        include_fk = True
        json_module = simplejson
# instance the class
propietario_schema = PropietarioSchema()

# TipoUsuario schema
class TipoUsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoUsuario
        include_fk = True
# instance the class
tipo_usuario_schema = TipoUsuarioSchema()

# Accion schema
class AccionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Accion
        include_fk = True
# instance the class
accion_schema = AccionSchema()

# AccionTipoUsuario schema
class AccionTipoUsuarioSchema(ma.SQLAlchemyAutoSchema):
    accion = ma.Nested(AccionSchema)
    tipo_usuario = ma.Nested(TipoUsuarioSchema)
    class Meta:
        model = AccionTipoUsuario
        include_fk = True
# instance the class
accion_tipo_usuario_schema = AccionTipoUsuarioSchema()

# Aficionado schema
class AficionadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aficionado
        include_fk = True
        json_module = simplejson
# instance the class
aficionado_schema = AficionadoSchema()

# PropietarioStud schema
class PropietarioStudSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PropietarioStud
        include_fk = True
        json_module = simplejson
# instance the class
propietario_stud_schema = PropietarioStudSchema()

# StudColor schema
class StudColorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudColor
        include_fk = True
# instance the class
stud_color_schema = StudColorSchema()

# Entrenador schema
class EntrenadorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Entrenador
        include_fk = True
        json_module = simplejson
# instance the class
entrenador_schema = EntrenadorSchema()

# Veterinario schema
class VeterinarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Veterinario
        include_fk = True
        json_module = simplejson
# instance the class
veterinario_schema = VeterinarioSchema()

# Usuario schema
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    # TipoUsuario
    tipo_usuario = ma.Nested(TipoUsuarioSchema)
    # Persona
    aficionado = ma.Nested(AficionadoSchema)
    entrenador = ma.Nested(EntrenadorSchema)
    jinete = ma.Nested(JineteSchema)
    propietario = ma.Nested(PropietarioSchema)
    veterinario = ma.Nested(VeterinarioSchema)
    class Meta:
        model = Usuario
        include_fk = True
        json_module = simplejson
# instance the class
usuario_schema = UsuarioSchema()

# Accion Usuario schema
class AccionUsuarioSchema(ma.SQLAlchemyAutoSchema):
    # Accion
    accion = ma.Nested(AccionSchema)
    # Usuario
    usuario = ma.Nested(UsuarioSchema)
    class Meta:
        model = AccionUsuario
        include_fk = True
        json_module = simplejson
# instance the class
accion_usuario_schema = AccionUsuarioSchema()

# Lugar schema
class LugarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lugar
        include_fk = True
# instance the class
lugar_schema = LugarSchema()

# HistoricoEntrenador schema
class HistoricoEntrenadorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoricoEntrenador
        include_fk = True
        json_module = simplejson
# instance the class
historico_entrenador_schema = HistoricoEntrenadorSchema()

# caballeriza schema
class CaballerizaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Caballeriza
        include_fk = True
        json_module = simplejson
# instance the class
caballeriza_schema = CaballerizaSchema()

# puesto schema
class PuestoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Puesto
        include_fk = True
        json_module = simplejson
# instance the class
puesto_schema = PuestoSchema()

# Hara schema
class HaraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hara
        include_fk = True
# instance the class
hara_schema = HaraSchema()

# HistoricoPuesto schema
class HistoricoPuestoSchema(ma.SQLAlchemyAutoSchema):
    # ejemplar
    ejemplar = ma.Nested(EjemplarSchema)
    # puesto
    puesto = ma.Nested(PuestoSchema)
    
    class Meta:
        model = HistoricoPuesto
        include_fk = True
        json_module = simplejson
# instance the class
historico_puesto_schema = HistoricoPuestoSchema()

# Binomio schema
class BinomioSchema(ma.SQLAlchemyAutoSchema):
    #ejemplar
    ejemplar = ma.Nested(lambda: EjemplarSchema(exclude=("parent","parent1",)))
    #padre
    jinete = ma.Nested(JineteSchema)
    class Meta:
        model = Binomio
        include_fk = True
        json_module = simplejson
# instance the class
binomio_schema = BinomioSchema()

# CategoriaCarrera schema
class CategoriaCarreraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CategoriaCarrera
        include_fk = True
# instance the class
categoria_carrera_schema = CategoriaCarreraSchema()

# TipoCarrera schema
class TipoCarreraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoCarrera
        include_fk = True
        json_module = simplejson
# instance the class
tipo_carrera_schema = TipoCarreraSchema()

# Pista schema
class PistaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pista
        include_fk = True
        json_module = simplejson
# instance the class
pista_schema = PistaSchema()

# PorcentajeDividendo schema
class PorcentajeDividendoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PorcentajeDividendo
        include_fk = True
        json_module = simplejson
# instance the class
porcentaje_dividendo_schema = PorcentajeDividendoSchema()

# CarreraPorcentajeDividendo schema
class CarreraPorcentajeDividendoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarreraPorcentajeDividendo
        include_fk = True
        json_module = simplejson
# instance the class
cpd_schema = CarreraPorcentajeDividendoSchema()

# Carrera schema
class CarreraSchema(ma.SQLAlchemyAutoSchema):
    #nested elements
    tipo_carrera = ma.Nested(TipoCarreraSchema)
    categoria_carrera = ma.Nested(CategoriaCarreraSchema)
    pista = ma.Nested(PistaSchema)
    class Meta:
        model = Carrera
        include_fk = True
        json_module = simplejson
# instance the class
carrera_schema = CarreraSchema()

# Implemento schema
class ImplementoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Implemento
        include_fk = True
# instance the class
implemento_schema = ImplementoSchema()

# Inscripcion schema
class InscripcionSchema(ma.SQLAlchemyAutoSchema):
    #nested elements
    binomio = ma.Nested(BinomioSchema)
    carrera = ma.Nested(CarreraSchema)
    implemento = ma.Nested(ImplementoSchema)
    class Meta:
        model = Inscripcion
        include_fk = True
        json_module = simplejson
# instance the class
inscripcion_schema = InscripcionSchema()

# CausaRetiro schema
class CausaRetiroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CausaRetiro
        include_fk = True
        json_module = simplejson
# instance the class
causa_retiro_schema = CausaRetiroSchema()

# Retiro schema
class RetiroSchema(ma.SQLAlchemyAutoSchema):

    causa_retiro = ma.Nested(CausaRetiroSchema)
    inscripcion = ma.Nested(InscripcionSchema)
    class Meta:
        model = Retiro
        include_fk = True
        json_module = simplejson
# instance the class
retiro_schema = RetiroSchema()

# TipoApuesta schema
class TipoApuestaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoApuesta
        include_fk = True
        json_module = simplejson
# instance the class
tipo_apuesta_schema = TipoApuestaSchema()

# Color schema
class ColorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Color
        include_fk = True
# instance the class
color_schema = ColorSchema()

#------------------------------------------------------------------------------------------

# endpoints -------------------------------------------------------------------------------

def deleteElement(model_object):
    try: 
        db.session.delete(model_object)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
        return False


def deleteInscripcion(inscripcion):
    # delete retiros
    retiros = Retiro.query.filter_by(fk_inscripcion=inscripcion.ins_clave)

    for retiro in retiros:
        if not deleteElement(retiro): 
            return False

    # delete inscripcion
    if deleteElement(inscripcion):
        return True
    else:
        return False


### Ejemplar ###

# RUD for one Ejemplar
class EjemplarEndPoint(Resource):
    def get(self, ejemplar_id):
        ejemplar = Ejemplar.query.get(ejemplar_id)
        # ejemplar does not exist
        if not ejemplar:
            abort(404, message="Ejemplar {} doesn't exist".format(ejemplar_id))

        return ejemplar_schema.dumps(ejemplar)

    def delete(self, ejemplar_id):
        ejemplar = Ejemplar.query.get(ejemplar_id)
        response = deleteElement(ejemplar)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, ejemplar_id):
        args = ejemplar_parser.parse_args()
        ejemplar = Ejemplar.query.get(ejemplar_id)
        #update the Ejemplar
        ejemplar.e_nombre = args["e_nombre"]
        ejemplar.e_color_pelaje = args["e_color_pelaje"]
        ejemplar.e_sexo = args["e_sexo"]
        ejemplar.e_fecha_nacimiento = args["e_fecha_nacimiento"]
        ejemplar.e_fecha_ing_hipo = args["e_fecha_ing_hipo"]
        ejemplar.e_peso = args["e_peso"]
        ejemplar.fk_haras = args["fk_haras"]
        ejemplar.fk_madre = args["fk_madre"]
        ejemplar.fk_padre = args["fk_padre"]
        ejemplar.fk_puesto = args["fk_puesto"]
        ejemplar.fk_caballeriza = args["fk_caballeriza"]

        try:
            db.session.commit()
            return ejemplar_schema.dumps(ejemplar), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(EjemplarEndPoint, '/ejemplares/<ejemplar_id>')

# list all ejemplares and create one
class EjemplarListEndPoint(Resource):
    def get(self):
        ejemplares = Ejemplar.query.all()
        return [ejemplar_schema.dumps(ejemplar) for ejemplar in ejemplares]

    def post(self):
        try:
            args = ejemplar_parser.parse_args()
            ejemplar = Ejemplar.create(**args)
            return ejemplar_schema.dumps(ejemplar), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(EjemplarListEndPoint, '/ejemplares')


### Entrenador ###

# RUD for one Entrenador
class EntrenadorEndPoint(Resource):
    def get(self, entrenador_id):
        entrenador = Entrenador.query.get(entrenador_id)
        # ejemplar does not exist
        if not entrenador:
            abort(404, message="Entrenador {} doesn't exist".format(entrenador_id))

        return entrenador_schema.dumps(entrenador)

    def delete(self, entrenador_id):
        entrenador = Entrenador.query.get(entrenador_id)
        response = deleteElement(entrenador)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, entrenador_id):
        args = entrenador_parser.parse_args()
        entrenador = Entrenador.query.get(entrenador_id)
        #update the Ejemplar
        entrenador.p_primer_nombre = args["p_primer_nombre"]
        entrenador.p_segundo_nombre = args["p_segundo_nombre"]
        entrenador.p_primer_apellido = args["p_primer_apellido"]
        entrenador.p_segundo_apellido = args["p_segundo_apellido"]
        entrenador.p_sexo = args["p_sexo"]
        entrenador.p_direccion = args["p_direccion"]
        entrenador.ent_fecha_ing_hipo = args["ent_fecha_ing_hipo"]
        entrenador.fk_lugar = args["fk_lugar"]

        try:
            db.session.commit()
            return entrenador_schema.dumps(entrenador), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(EntrenadorEndPoint, '/entrenadores/<entrenador_id>')

# list all entrenadores and create one
class EntrenadorListEndPoint(Resource):
    def get(self):
        entrenadores = Entrenador.query.all()
        return [entrenador_schema.dumps(entrenador) for entrenador in entrenadores]

    def post(self):
        try:
            args = entrenador_parser.parse_args()
            entrenador = Entrenador.create(**args)
            return entrenador_schema.dumps(entrenador), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(EntrenadorListEndPoint, '/entrenadores')


### Jinete ###

# RUD for one jinete
class JineteEndPoint(Resource):
    def get(self, jinete_id):
        jinete = Jinete.query.get(jinete_id)
        # ejemplar does not exist
        if not jinete:
            abort(404, message="Jinete {} doesn't exist".format(jinete_id))

        return jinete_schema.dumps(jinete)

    def delete(self, jinete_id):
        jinete = Jinete.query.get(jinete_id)
        response = deleteElement(jinete)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, jinete_id):
        args = jinete_parser.parse_args()
        jinete = Jinete.query.get(jinete_id)
        #update the Jinete
        jinete.p_primer_nombre = args["p_primer_nombre"]
        jinete.p_segundo_nombre = args["p_segundo_nombre"]
        jinete.p_primer_apellido = args["p_primer_apellido"]
        jinete.p_segundo_apellido = args["p_segundo_apellido"]
        jinete.p_sexo = args["p_sexo"]
        jinete.p_direccion = args["p_direccion"]
        jinete.j_altura = args["j_altura"]
        jinete.j_peso_al_ingresar = args["j_peso_al_ingresar"]
        jinete.j_peso_actual = args["j_peso_actual"]
        jinete.j_rango = args["j_rango"]
        jinete.j_fecha_nacimiento = args["j_fecha_nacimiento"]
        jinete.fk_lugar = args["fk_lugar"]

        try:
            db.session.commit()
            return jinete_schema.dumps(jinete), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(JineteEndPoint, '/jinetes/<jinete_id>')

# list all jinetes and create one
class JineteListEndPoint(Resource):
    def get(self):
        jinetes = Jinete.query.all()
        return [jinete_schema.dumps(jinete) for jinete in jinetes]

    def post(self):
        try:
            args = jinete_parser.parse_args()
            jinete = Jinete.create(**args)
            return jinete_schema.dumps(jinete), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(JineteListEndPoint, '/jinetes')


### Stud ###

# RUD for one stud
class StudEndPoint(Resource):
    def get(self, stud_id):
        stud = Stud.query.get(stud_id)
        # ejemplar does not exist
        if not stud:
            abort(404, message="Stud {} doesn't exist".format(stud_id))

        return stud_schema.dump(stud)

    def delete(self, stud_id):
        stud = Stud.query.get(stud_id)
        #first get all the tables that include them and delete the matches in them
        # StudPropietario
        propietariosStud = PropietarioStud.query.filter_by(fk_stud=stud_id)
        for element in propietariosStud:
            response = deleteElement(element)
            if not response: 
                print("Oh no error al eliminar StudPropietario")
                break
        # StudColor
        coloresStud = StudColor.query.filter_by(fk_stud=stud_id)
        for element in coloresStud:
            response = deleteElement(element)
            if not response: 
                print("Oh no error al eliminar StudColor")
                break
        # delete the stud
        response = deleteElement(stud)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, stud_id):
        args = stud_parser.parse_args()
        stud = Stud.query.get(stud_id)
        #update the Stud
        stud.s_nombre = args["s_nombre"]
        stud.s_fecha_creacion = args["s_fecha_creacion"]

        try:
            db.session.commit()
            return stud_schema.dump(stud), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(StudEndPoint, '/studs/<stud_id>')

# list all studs and create one
class StudListEndPoint(Resource):
    def get(self):
        studs = Stud.query.all()
        return [stud_schema.dump(stud) for stud in studs]

    def post(self):
        try:
            args = stud_parser.parse_args()
            stud = Stud.create(**args)
            return stud_schema.dump(stud), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(StudListEndPoint, '/studs')


### Carrera ###

# RUD for one stud
class CarreraEndPoint(Resource):
    def get(self, carrera_id):
        carrera = Carrera.query.get(carrera_id)
        # ejemplar does not exist
        if not carrera:
            abort(404, message="Carrera {} doesn't exist".format(carrera_id))

        return carrera_schema.dumps(carrera)

    def delete(self, carrera_id):
        # get the carrera
        carrera = Carrera.query.get(carrera_id)

        # delete all the inscriptions
        inscriptions = Inscripcion.query.filter_by(fk_carrera=carrera_id)
        for element in inscriptions:
            deleted = deleteInscripcion(element)
            if not deleted: return 'Can not delete, incripcion', 500
        # delete carrera porcentaje dividendo
        cpds = CarreraPorcentajeDividendo.query.filter_by(fk_carrera=carrera_id)
        for element in cpds:
            deleted = deleteElement(element)
            if not deleted: return 'Can not delete, carrera porcentaje dividendo', 500
        # delete the carrera
        response = deleteElement(carrera)

        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, carrera_id):
        args = carrera_parser.parse_args()
        carrera = Carrera.query.get(carrera_id)
        #update the Carrera
        carrera.c_nombre = args["c_nombre"]
        carrera.c_fecha = args["c_fecha"]
        carrera.c_hora = args["c_hora"]
        carrera.c_num_llamado = args["c_num_llamado"]
        carrera.c_pull_dinero_total = args["c_pull_dinero_total"]
        carrera.c_distancia = args["c_distancia"]
        carrera.c_comentario = args["c_comentario"]
        carrera.fk_tipo_carrera = args["fk_tipo_carrera"]
        carrera.fk_categoria_carrera = args["fk_categoria_carrera"]
        carrera.fk_pista = args["fk_pista"]

        # delete carrera porcentaje dividendo
        cpds = CarreraPorcentajeDividendo.query.filter_by(fk_carrera=carrera_id)
        for element in cpds:
            deleted = deleteElement(element)
            if not deleted: return 'Can not delete, carrera porcentaje dividendo', 500

        try:
            db.session.commit()
            return carrera_schema.dumps(carrera), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(CarreraEndPoint, '/carreras/<carrera_id>')

# list all carreras and create one
class CarreraListEndPoint(Resource):
    def get(self):
        carreras = Carrera.query.all()
        return [carrera_schema.dumps(carrera) for carrera in carreras]

    def post(self):
        try:
            args = carrera_parser.parse_args()
            carrera = Carrera.create(**args)
            return carrera_schema.dumps(carrera), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(CarreraListEndPoint, '/carreras')


### Propietario ###

# RUD for one propietario
class PropietarioEndPoint(Resource):
    def get(self, propietario_id):
        propietario = Propietario.query.get(propietario_id)
        # ejemplar does not exist
        if not propietario:
            abort(404, message="Propietario {} doesn't exist".format(propietario_id))

        return propietario_schema.dumps(propietario)

    def delete(self, propietario_id):
        propietario = Propietario.query.get(propietario_id)
        response = deleteElement(propietario)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, propietario_id):
        args = propietario_parser.parse_args()
        propietario = Propietario.query.get(propietario_id)
        #update the Jinete
        propietario.p_primer_nombre = args["p_primer_nombre"]
        propietario.p_segundo_nombre = args["p_segundo_nombre"]
        propietario.p_primer_apellido = args["p_primer_apellido"]
        propietario.p_segundo_apellido = args["p_segundo_apellido"]
        propietario.p_sexo = args["p_sexo"]
        propietario.p_direccion = args["p_direccion"]
        propietario.pr_correo = args["pr_correo"]
        propietario.pr_fecha_nacimiento = args["pr_fecha_nacimiento"]
        propietario.fk_lugar = args["fk_lugar"]

        try:
            db.session.commit()
            return propietario_schema.dumps(propietario), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(PropietarioEndPoint, '/propietarios/<propietario_id>')

# list all propietarios and create one
class PropietarioListEndPoint(Resource):
    def get(self):
        propietarios = Propietario.query.all()
        return [propietario_schema.dumps(propietario) for propietario in propietarios]

    def post(self):
        try:
            args = propietario_parser.parse_args()
            propietario = Propietario.create(**args)
            return propietario_schema.dumps(propietario), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(PropietarioListEndPoint, '/propietarios')


### Tipo_Usuario ###

# RUD for one TipoUsuario
class TipoUsuarioEndPoint(Resource):
    def get(self, tipo_usuario_id):
        tipo_usuario = TipoUsuario.query.get(tipo_usuario_id)
        # ejemplar does not exist
        if not tipo_usuario:
            abort(404, message="Stud {} doesn't exist".format(tipo_usuario_id))

        return tipo_usuario_schema.dump(tipo_usuario)

    def delete(self, tipo_usuario_id):
        tipo_usuario = TipoUsuario.query.get(tipo_usuario_id)

        # verify if some user is using it
        users = Usuario.query.filter_by(fk_tipo_usuario=tipo_usuario_id).all()
        if users: return 'Can not delete tipo usuario, is being used', 500

        # delete all the assignments of actions
        actions = AccionTipoUsuario.query.filter_by(fk_tipousuario=tipo_usuario_id)
        for element in actions: 
            deleted = deleteElement(element)
            if not deleted: return 'Can not delete tipo usuario accion', 500

        response = deleteElement(tipo_usuario)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, tipo_usuario_id):
        args = tipo_usuario_parser.parse_args()
        tipo_usuario = TipoUsuario.query.get(tipo_usuario_id)
        #update the Stud
        tipo_usuario.tu_nombre = args["tu_nombre"]

        # delete all the assignments of actions
        actions = AccionTipoUsuario.query.filter_by(fk_tipousuario=tipo_usuario_id)
        for element in actions: 
            deleted = deleteElement(element)
            if not deleted: return 'Can not delete tipo usuario accion', 500

        try:
            db.session.commit()
            return tipo_usuario_schema.dump(tipo_usuario), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(TipoUsuarioEndPoint, '/tipos-usuarios/<tipo_usuario_id>')

# list all TipoUsuario and create one
class TipoUsuarioListEndPoint(Resource):
    def get(self):
        tipos_usuarios = TipoUsuario.query.all()
        return [tipo_usuario_schema.dump(tipo_usuario) for tipo_usuario in tipos_usuarios]

    def post(self):
        try:
            args = tipo_usuario_parser.parse_args()
            tipo_usuario = TipoUsuario.create(**args)
            return tipo_usuario_schema.dump(tipo_usuario), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(TipoUsuarioListEndPoint, '/tipos-usuarios')


### Accion_Tipo_Usuario ###

# RUD for one AccionTipoUsuario
class AccionTipoUsuarioEndPoint(Resource):
    def get(self, accion_tipo_usuario_id):
        accion_tipo_usuario = AccionTipoUsuario.query.get(accion_tipo_usuario_id)
        # ejemplar does not exist
        if not accion_tipo_usuario:
            abort(404, message="Accion tipo usuario {} doesn't exist".format(accion_tipo_usuario_id))

        return accion_tipo_usuario_schema.dump(accion_tipo_usuario)

    def delete(self, accion_tipo_usuario_id):
        accion_tipo_usuario = AccionTipoUsuario.query.get(accion_tipo_usuario_id)
        response = deleteElement(accion_tipo_usuario)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, accion_tipo_usuario_id):
        args = accion_tipo_usuario_parser.parse_args()
        accion_tipo_usuario = AccionTipoUsuario.query.get(accion_tipo_usuario_id)
        #update the Stud
        accion_tipo_usuario.fk_tipousuario = args["fk_tipousuario"]
        accion_tipo_usuario.fk_accion = args["fk_accion"]

        try:
            db.session.commit()
            return accion_tipo_usuario_schema.dump(accion_tipo_usuario), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(AccionTipoUsuarioEndPoint, '/accion/tipo/usuario/<accion_tipo_usuario_id>')

# list all AccionTipoUsuario and create one
class AccionTipoUsuarioListEndPoint(Resource):
    def get(self):
        acciones_tipo_usuario = AccionTipoUsuario.query.all()
        return [accion_tipo_usuario_schema.dump(accion_tipo_usuario) for accion_tipo_usuario in acciones_tipo_usuario]

    def post(self):
        try:
            args = accion_tipo_usuario_parser.parse_args()
            accion_tipo_usuario = AccionTipoUsuario.create(**args)
            return accion_tipo_usuario_schema.dump(accion_tipo_usuario), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(AccionTipoUsuarioListEndPoint, '/acciones/tipo/usuario')


### Usuario ###

# RUD for one Usuario
class UsuarioEndPoint(Resource):
    def get(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        # ejemplar does not exist
        if not usuario:
            abort(404, message="Usuario {} doesn't exist".format(usuario_id))

        return usuario_schema.dumps(usuario)

    def delete(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        response = deleteElement(usuario)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, usuario_id):
        args = usuario_parser.parse_args()
        usuario = Usuario.query.get(usuario_id)
        #update the Stud
        usuario.u_password = args["u_password"]
        usuario.u_fecha_registro = args["u_fecha_registro"]
        usuario.fk_entrenador = args["fk_entrenador"]
        usuario.fk_propietario = args["fk_propietario"]
        usuario.fk_jinete = args["fk_jinete"]
        usuario.fk_veterinario = args["fk_veterinario"]
        usuario.fk_aficionado = args["fk_aficionado"]
        usuario.fk_tipo_usuario = args["fk_tipo_usuario"]
        
        try:
            db.session.commit()
            return usuario_schema.dumps(usuario), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(UsuarioEndPoint, '/usuarios/<usuario_id>')

# list all Usuario and create one
class UsuarioListEndPoint(Resource):
    def get(self):
        usuarios = Usuario.query.all()
        return [usuario_schema.dumps(usuario) for usuario in usuarios]

    def post(self):
        try:
            args = usuario_parser.parse_args()
            usuario = Usuario.create(**args)
            return usuario_schema.dumps(usuario), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(UsuarioListEndPoint, '/usuarios')


### Lugar ###
class LugarListEndPoint(Resource):
    def get(self):
        lugares = Lugar.query.all()
        return [lugar_schema.dump(lugar) for lugar in lugares]
# add the endpoint ot the api
api.add_resource(LugarListEndPoint, '/lugares')


### Accion_Usuario ###

# RUD for one AccionUsuario
class AccionUsuarioEndPoint(Resource):
    def get(self, accion_usuario_id):
        accion_usuario = AccionUsuario.query.get(accion_usuario_id)
        # ejemplar does not exist
        if not accion_usuario:
            abort(404, message="Accion usuario {} doesn't exist".format(accion_usuario_id))

        return accion_tipo_usuario_schema.dump(accion_usuario)

    def delete(self, accion_usuario_id):
        accion_usuario = AccionUsuario.query.get(accion_usuario_id)
        response = deleteElement(accion_usuario)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, accion_usuario_id):
        args = accion_usuario_parser.parse_args()
        accion_usuario = AccionUsuario.query.get(accion_usuario_id)
        #update the accion_usuario
        accion_usuario.fk_tipousuario = args["fk_tipousuario"]
        accion_usuario.fk_accion = args["fk_accion"]

        try:
            db.session.commit()
            return accion_usuario_schema.dump(accion_usuario), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(AccionUsuarioEndPoint, '/accion-usuarios/<accion_usuario_id>')

# list all AccionTipoUsuario and create one
class AccionUsuarioListEndPoint(Resource):
    def get(self):
        acciones_usuarios = AccionUsuario.query.all()
        return [accion_usuario_schema.dump(accion_usuario) for accion_usuario in acciones_usuarios]

    def post(self):
        try:
            args = accion_usuario_parser.parse_args()
            accion_usuario = AccionUsuario.create(**args)
            return accion_usuario_schema.dump(accion_usuario), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(AccionUsuarioListEndPoint, '/accion-usuarios')


### Permisos para el tipo de Usuario ###
class PermisosTipoUsuarioEndPoint(Resource):
    def get(self, tipo_usuario_id):
        acciones_tipo_usuario = AccionTipoUsuario.query.filter_by(fk_tipousuario=tipo_usuario_id)

        permisos = {}
        for element in acciones_tipo_usuario:

            accion = element.accion.acc_nombre
            tabla_objectivo = element.accion.acc_tabla_objetivo

            if tabla_objectivo in permisos.keys():
                permisos[tabla_objectivo].append(accion)
            else:
                permisos.update({
                    tabla_objectivo: [accion]
                })

        # acciones_tipo_usuario empty
        if not acciones_tipo_usuario:
            abort(404, message="User type {} does not have permissions".format(tipo_usuario_id))

        # To return all the actions from DB
        # [accion_schema.dump(element.accion) for element in acciones_tipo_usuario]
        return simplejson.dumps(permisos), 200
# add the endpoint ot the api
api.add_resource(PermisosTipoUsuarioEndPoint, '/permisos-tipo-usuario/<tipo_usuario_id>')


### Login ###
class LogInEndPoint(Resource):    
    def post(self):
        try:
            args = request.json
            # select the values
            correo = args['u_correo_e']
            password = args['u_password']
            # make the query searching from correo
            usuario = {}
            try:
                usuario = Usuario.query.filter_by(u_correo_e=correo).first()
            except BaseException as e:
                print(e)
                usuario = None
            print(usuario)

            # if correo does not exist
            if not usuario: 
                return simplejson.dumps({
                        "msg": "No existe usuario con este correo",
                        "correo": False,
                        "password": False
                    }), 404
            
            if usuario.u_password != password:
                return simplejson.dumps({
                        "msg": "No existe usuario con este correo",
                        "correo": True,
                        "password": False
                    }), 404

            print(args)
            return usuario_schema.dumps(usuario), 200
        except BaseException as e:
            print(e)
            return 'Failed', 400
    
# add the endpoint ot the api
api.add_resource(LogInEndPoint, '/login')


### HistoricoEntrenador ###

# RUD for one historico
class HistoricoEntrenadorEndPoint(Resource):
    def delete(self, historico_id):
        historico = HistoricoEntrenador.query.get(historico_id)
        response = deleteElement(historico)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400
# add the endpoint ot the api
api.add_resource(HistoricoEntrenadorEndPoint, '/historico/entrenador/<historico_id>')

# list all historicos and create one
class HistoricoEntrenadorListEndPoint(Resource):
    def get(self):
        historicos = HistoricoEntrenador.query.all()
        return [historico_entrenador_schema.dumps(historico) for historico in historicos]

    def post(self):
        try:
            args = historico_entrenador_parser.parse_args()
            print(args)
            historico = HistoricoEntrenador.create(**args)
            return historico_entrenador_schema.dumps(historico), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(HistoricoEntrenadorListEndPoint, '/historicos/entrenadores')


### PropietarioStud ###

# RUD for one PropietarioStud
class PropietarioStudEndPoint(Resource):
    def delete(self, element_id):
        element = PropietarioStud.query.get(element_id)
        response = deleteElement(element)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400
# add the endpoint ot the api
api.add_resource(PropietarioStudEndPoint, '/propietario/stud/<element_id>')

# list all historicos and create one
class PropietarioStudListEndPoint(Resource):
    def get(self):
        elements = PropietarioStud.query.all()
        return [propietario_stud_schema.dumps(element) for element in elements]

    def post(self):
        try:
            args = propietario_stud_parser.parse_args()
            element = PropietarioStud.create(**args)
            return propietario_stud_schema.dumps(element), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(PropietarioStudListEndPoint, '/propietarios/studs')


### StudColor ###

# RUD for one StudColor
class StudColorEndPoint(Resource):
    def delete(self, element_id):
        element = StudColor.query.get(element_id)
        response = deleteElement(element)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400
# add the endpoint ot the api
api.add_resource(StudColorEndPoint, '/color/stud/<element_id>')

# list all historicos and create one
class StudColorListEndPoint(Resource):
    def get(self):
        elements = StudColor.query.all()
        return [stud_color_schema.dump(element) for element in elements]

    def post(self):
        try:
            args = color_stud_parser.parse_args()
            element = StudColor.create(**args)
            return stud_color_schema.dump(element), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(StudColorListEndPoint, '/colores/studs')


### Caballeriza ###
# shows a list of all caballerizas
class CaballerizaListEndPoint(Resource):
    def get(self):
        caballerizas = Caballeriza.query.all()
        return [caballeriza_schema.dumps(caballeriza) for caballeriza in caballerizas]

# add the endpoint ot the api
api.add_resource(CaballerizaListEndPoint, '/caballerizas')


### Puesto ###
class PuestoEndPoint(Resource):
    def get(self, caballeriza_id):
        puestos = Puesto.query.filter_by(fk_caballeriza=caballeriza_id)
        # ejemplar does not exist
        if not puestos:
            abort(404, message="Error con los puestos de la caballeriza")

        return [puesto_schema.dumps(puesto) for puesto in puestos]

# add the endpoint ot the api
api.add_resource(PuestoEndPoint, '/puestos/<caballeriza_id>')

# shows a list of all caballerizas
class PuestoListEndPoint(Resource):
    def get(self):
        puestos = Puesto.query.all()
        return [puesto_schema.dumps(puesto) for puesto in puestos]

# add the endpoint ot the api
api.add_resource(PuestoListEndPoint, '/puestos')


### Hara ###
# shows a list of all caballerizas
class HaraListEndPoint(Resource):
    def get(self):
        haras = Hara.query.all()
        return [hara_schema.dump(hara) for hara in haras]

# add the endpoint ot the api
api.add_resource(HaraListEndPoint, '/haras')


### HistoricoPuesto ###

# RUD for one HistoricoPuesto
class HistoricoPuestoEndPoint(Resource):
    def put(self, element_id):
        historico = HistoricoPuesto.query.filter_by(fk_puesto=element_id, hp_fecha_final=None).first()
        #update the accion_usuario
        historico.hp_fecha_final = datetime.datetime.now()

        try:
            db.session.commit()
            return historico_puesto_schema.dumps(historico), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400

    def delete(self, element_id):
        element = HistoricoPuesto.query.get(element_id)
        response = deleteElement(element)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400
# add the endpoint ot the api
api.add_resource(HistoricoPuestoEndPoint, '/historico/puesto/<element_id>')

# list all historicos and create one
class HistoricoPuestoListEndPoint(Resource):
    def get(self):
        elements = HistoricoPuesto.query.all()
        return [historico_puesto_schema.dumps(element) for element in elements]

    def post(self):
        try:
            args = historico_puesto_parser.parse_args()
            element = HistoricoPuesto.create(**args)
            return historico_puesto_schema.dumps(element), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(HistoricoPuestoListEndPoint, '/historicos/puestos')


### Binomio ###

# RUD for one binomio
class BinomioEndPoint(Resource):
    def get(self, binomio_id):
        binomio = Binomio.query.get(binomio_id)
        # ejemplar does not exist
        if not binomio:
            abort(404, message="Binomio {} doesn't exist".format(binomio_id))

        return binomio_schema.dumps(binomio)

    def delete(self, binomio_id):
        binomio = Binomio.query.get(binomio_id)
        response = deleteElement(binomio)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, binomio_id):
        args = binomio_parser.parse_args()
        binomio = Binomio.query.get(binomio_id)
        #update the binomio
        binomio.bi_clave = args["bi_clave"]
        binomio.fk_ejemplar = args["fk_ejemplar"]
        binomio.fk_jinete = args["fk_jinete"]
        binomio.bi_jinete_peso = args["bi_jinete_peso"]
        binomio.bi_ejemplar_peso = args["bi_ejemplar_peso"]
        

        try:
            db.session.commit()
            return binomio_schema.dumps(binomio), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(BinomioEndPoint, '/binomios/<binomio_id>')

# list all binomios and create one
class BinomioListEndPoint(Resource):
    def get(self):
        binomios = Binomio.query.all()
        return [binomio_schema.dumps(binomio) for binomio in binomios]

    def post(self):
        try:
            args = binomio_parser.parse_args()
            # verify that the binomio dos not exist
            exists = Binomio.query.filter_by(fk_ejemplar=args["fk_ejemplar"], fk_jinete=args["fk_jinete"]).first()
            
            if exists:
                return 'Failed, binomio already exists', 400

            binomio = Binomio.create(**args)
            return binomio_schema.dumps(binomio), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(BinomioListEndPoint, '/binomios')


### NumLlamadoCarrera ###
# shows a list of num llamado for a date
class NumLlamadoCarreraListEndPoint(Resource):
    def get(self, date):
        carreras_in_date = Carrera.query.filter_by(c_fecha=date)
        
        return [carrera_schema.dumps(element) for element in carreras_in_date]
# add the endpoint ot the api
api.add_resource(NumLlamadoCarreraListEndPoint, '/carrera/cun/llamado/<date>')


### TipoCarrera ###
# shows a list of all TipoCarrera
class TipoCarreraListEndPoint(Resource):
    def get(self):
        elements = TipoCarrera.query.all()
        return [tipo_carrera_schema.dumps(element) for element in elements]
# add the endpoint ot the api
api.add_resource(TipoCarreraListEndPoint, '/tipos/carrera')


### CategoriaCarrera ###
# shows a list of all TipoCarrera
class CategoriaCarreraListEndPoint(Resource):
    def get(self):
        elements = CategoriaCarrera.query.all()
        return [categoria_carrera_schema.dump(element) for element in elements]
# add the endpoint ot the api
api.add_resource(CategoriaCarreraListEndPoint, '/categorias/carrera')


### Pista ###
# shows a list of all TipoCarrera
class PistaListEndPoint(Resource):
    def get(self):
        elements = Pista.query.all()
        return [pista_schema.dumps(element) for element in elements]
# add the endpoint ot the api
api.add_resource(PistaListEndPoint, '/pistas')


### PorcentajeDividendo ###
# shows a list of all TipoCarrera
class PorcentajeDividendoListEndPoint(Resource):
    def get(self):
        elements = PorcentajeDividendo.query.all()
        return [porcentaje_dividendo_schema.dumps(element) for element in elements]
# add the endpoint ot the api
api.add_resource(PorcentajeDividendoListEndPoint, '/porcentajes/dividendo')


### CarreraPorcentajeDividendo ###

# create CarreraPorcentajeDividendo
class CarreraPorcentajeDividendoListEndPoint(Resource):
    def get(self):
        elements = CarreraPorcentajeDividendo.query.all()
        return [cpd_schema.dumps(element) for element in elements]

    def post(self):
        try:
            args = cpd_parser.parse_args()

            element = CarreraPorcentajeDividendo.create(**args)
            return cpd_schema.dumps(element), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(CarreraPorcentajeDividendoListEndPoint, '/carrera/porcentaje/dividendo')


### Inscripcion ###

# RUD for one Inscripcion
class InscripcionEndPoint(Resource):
    def get(self, inscripcion_id):
        inscripcion = Inscripcion.query.get(inscripcion_id)
        # ejemplar does not exist
        if not inscripcion:
            abort(404, message="Inscripcion {} doesn't exist".format(inscripcion_id))

        return inscripcion_schema.dumps(inscripcion)

    def delete(self, inscripcion_id):
        # get the carrera
        inscripcion = Inscripcion.query.get(inscripcion_id)
        response = deleteElement(inscripcion)

        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, carrera_id):
        args = inscripcion_parser.parse_args()
        inscripcion = Inscripcion.query.get(carrera_id)

        #update the inscripcion
        inscripcion.ins_num_gualdrapa = args["ins_num_gualdrapa"]
        inscripcion.ins_puesto_pista = args["ins_puesto_pista"]
        inscripcion.ins_fecha = args["ins_fecha"]
        inscripcion.ins_ejemplar_favorito = args["ins_ejemplar_favorito"]
        inscripcion.ins_precio_reclamado = args["ins_precio_reclamado"]
        inscripcion.fk_carrera = args["fk_carrera"]
        inscripcion.fk_binomio = args["fk_binomio"]
        inscripcion.fk_implemento = args["fk_implemento"]

        try:
            db.session.commit()
            return inscripcion_schema.dumps(inscripcion), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(InscripcionEndPoint, '/inscripciones/<inscripcion_id>')

# list all Inscripciones and create one
class InscripcionListEndPoint(Resource):
    def get(self):
        elements = Inscripcion.query.all()
        return [inscripcion_schema.dumps(element) for element in elements]

    def post(self):
        try:
            args = inscripcion_parser.parse_args()

            # verify space in carrera
            inscripciones = Inscripcion.query.filter_by(fk_carrera=args["fk_carrera"]).all()
            inscripciones_len = len(inscripciones)
            if inscripciones_len==12:
                return 'Carrera full', 400
            
            for inscripcion in inscripciones: 
                if inscripcion.fk_binomio==int(args["fk_binomio"]):
                    return 'Ya se encuentra registrado', 400
            
            # set the gualdrapa and puesto pista
            args["ins_num_gualdrapa"] = inscripciones_len+1
            args["ins_puesto_pista"] = inscripciones_len+1
            args["fk_implemento"] = 11

            inscripcion = Inscripcion.create(**args)
            return inscripcion_schema.dumps(inscripcion), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(InscripcionListEndPoint, '/inscripciones')

# list all Inscripciones and create one
class ActiveInscripciones(Resource):
    def get(self):

        filtered_inscripciones = []

        today_date = datetime.datetime.now()
        aux_date = f'{today_date.year}-{today_date.month}-{today_date.day}'

        inscripciones = db.engine.execute(f'''
        SELECT  I.INS_Clave
        FROM    Inscripcion I, Carrera C
        WHERE   I.FK_Carrera=C.C_Clave          and
                '{aux_date}'<=C.C_Fecha         and 
                I.INS_Clave NOT IN (
                    SELECT  R.FK_Inscripcion
                    FROM    Retiro R
                )
        ''')

        for element in inscripciones:
            filtered_inscripciones.append(Inscripcion.query.get(element[0]))

        return [inscripcion_schema.dumps(element) for element in filtered_inscripciones]
# add the endpoint ot the api
api.add_resource(ActiveInscripciones, '/inscripciones/activas')

### CausaRetiro ###
# shows a list of all CausaRetiro
class CausaRetiroListEndPoint(Resource):
    def get(self):
        causas_retiros = CausaRetiro.query.all()
        return [causa_retiro_schema.dumps(causa_retiro) for causa_retiro in causas_retiros]
# add the endpoint ot the api
api.add_resource(CausaRetiroListEndPoint, '/causas/retiros')

### Retiro ###

# create and get all RetiroSchema 
class RetiroEndPoint(Resource):
    def get(self):
        elements = Retiro.query.all()
        return [retiro_schema.dumps(element) for element in elements]

    def post(self):
        try:
            args = retiro_parser.parse_args()

            element = Retiro.create(**args)
            return retiro_schema.dumps(element), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(RetiroEndPoint, '/retiros')

# get victories of a ejemplar
class VictoriesListEndPoint(Resource):
    def get(self, ejemplar_id):
        try:
            elements =  db.engine.execute(f'''
                SELECT COUNT(B.FK_Ejemplar), B.FK_Ejemplar
                FROM Binomio B, Inscripcion I, Resultado_Ejemplar RE 
                WHERE   B.FK_Ejemplar={ejemplar_id}     and
                        I.FK_Binomio=B.BI_Clave         and
                        RE.FK_Inscripcion=I.INS_Clave   and
                        RE.RES_Orden_Llegada=1
                GROUP BY B.FK_Ejemplar;
            ''')

            victories = (int(ejemplar_id), 0)
            for element in elements:
                if element: 
                    victories = (element[1], element[0])
                else:
                    victories = (element[1], element[0])
            
            return simplejson.dumps(victories), 200

        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(VictoriesListEndPoint, '/victories/<ejemplar_id>')

# get victories for all binomios
class BinomiosVictoriesEndPoint(Resource):
    def get(self):
        try:
            binomios = Binomio.query.all()
            ejemplares_victories = {}
            
            for binomio in binomios:

                elements =  db.engine.execute(f'''
                    SELECT COUNT(B.FK_Ejemplar), B.FK_Ejemplar
                    FROM Binomio B, Inscripcion I, Resultado_Ejemplar RE 
                    WHERE   B.FK_Ejemplar={binomio.fk_ejemplar}     and
                            I.FK_Binomio=B.BI_Clave         and
                            RE.FK_Inscripcion=I.INS_Clave   and
                            RE.RES_Orden_Llegada=1
                    GROUP BY B.FK_Ejemplar;
                ''')

                ejemplares_victories[binomio.fk_ejemplar] = 0
                for element in elements:
                    if element: 
                        ejemplares_victories[binomio.fk_ejemplar] = element[0]
                    else:
                        ejemplares_victories[binomio.fk_ejemplar] = element[0]
            
            return simplejson.dumps(ejemplares_victories), 200

        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(BinomiosVictoriesEndPoint, '/ejemplares/victories')

# get carrera for ejemplar
class CarrerasForEjemplarEndPoint(Resource):
    def get(self, ejemplar_id, ejemplar_age, ejemplar_wins):
        try:
            ejemplar = Ejemplar.query.get(ejemplar_id)
            filtered_carreras = []

            today_date = datetime.datetime.now()
            aux_date = f'{today_date.year}-{today_date.month}-{today_date.day}'

            carreras = db.engine.execute(f'''
            SELECT  C.C_Clave, C.C_Nombre, C.C_Fecha, C.C_Hora, 
                    C.C_Num_Llamado, C.C_Pull_Dinero_Total, 
                    C.C_Distancia, C.C_Comentario, C.FK_Tipo_Carrera, 
                    C.FK_Categoria_Carrera, C.FK_Pista
            FROM    Carrera C, Tipo_Carrera TC
            WHERE   C.FK_Tipo_Carrera=TC.TC_Clave                                           and
                    {ejemplar_age} BETWEEN TC.TC_Edad_Minima AND TC.TC_Edad_Maxima          and
                    {ejemplar_wins} BETWEEN TC.TC_Victoria_Minima AND TC.TC_Victoria_Maxima and
                    '{ejemplar.e_sexo}'=TC.TC_Sexo                                          and
                    '{aux_date}'<=C.C_Fecha
            ''')

            '''for element in carreras:
                print(element)
                #filtered_carreras.append(element)
                filtered_carreras.append({
                    'c_clave':element[0],
                    'c_nombre':element[1],
                    'c_fecha':element[2],
                    'c_hora':element[3],
                    'c_num_llamado':element[4],
                    'c_pull_dinero_total':element[5],
                    'c_distancia':element[6],
                    'c_comentario':element[7],
                    'fk_tipo_carrera':element[8],
                    'fk_categoria_carrera':element[9],
                    'fk_pista':element[10],
                })'''
            
            for element in carreras:
                filtered_carreras.append(Carrera.query.get(element[0])) 
            
            return [carrera_schema.dumps(carrera) for carrera in filtered_carreras], 200

        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(CarrerasForEjemplarEndPoint, '/carreras/ejemplar/<ejemplar_id>/<ejemplar_age>/<ejemplar_wins>')


### Accion ###
# shows a list of all colors, and lets you POST to add new colors
class AccionListEndPoint(Resource):
    def get(self):
        acciones = Accion.query.all()
        return [accion_schema.dump(accion) for accion in acciones]

# add the endpoint ot the api
api.add_resource(AccionListEndPoint, '/acciones')


### Tipo Apuesta ###

# RUD for one tipo apuesta
class TipoApuestaEndPoint(Resource):
    def get(self, tipo_apuesta_id):
        tipo_apuesta = TipoApuesta.query.get(tipo_apuesta_id)
        # ejemplar does not exist
        if not tipo_apuesta:
            abort(404, message="Tipo apuesta {} doesn't exist".format(tipo_apuesta_id))

        return tipo_apuesta_schema.dumps(tipo_apuesta)

    def delete(self, tipo_apuesta_id):
        tipo_apuesta = TipoApuesta.query.get(tipo_apuesta_id)

        # delete all apuestas referencing it
        apuestas = Apuesta.query.filter_by(fk_tipoapuesta=tipo_apuesta.ta_clave)
        for apuesta in apuestas:
            try:
                apuesta.fk_tipoapuesta = None
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return 'Could not be updated', 400

        response = deleteElement(tipo_apuesta)
        if response:
            return 'Deleted', 200
        else:
            return 'Can not delete', 400

    def put(self, tipo_apuesta_id):
        args = tipo_apuesta_parser.parse_args()
        tipo_apuesta = TipoApuesta.query.get(tipo_apuesta_id)
        #update tipoapuesta
        tipo_apuesta.ta_nombre = args["ta_nombre"]
        tipo_apuesta.ta_precio = args["ta_precio"]
        tipo_apuesta.ta_saldo_minimo = args["ta_saldo_minimo"]
        tipo_apuesta.ta_multiplicador = args["ta_multiplicador"]
        tipo_apuesta.ta_precio_jugada_adicional = args["ta_precio_jugada_adicional"]
        tipo_apuesta.ta_cant_minima_caballos_necesaria_en_carrera = args["ta_cant_minima_caballos_necesaria_en_carrera"]
        tipo_apuesta.ta_cant_maxima_caballos_por_carrera = args["ta_cant_maxima_caballos_por_carrera"]
        tipo_apuesta.ta_cant_maxima_caballos = args["ta_cant_maxima_caballos"]
        tipo_apuesta.ta_cant_valida_ultimas_carreras_programa = args["ta_cant_valida_ultimas_carreras_programa"]
        tipo_apuesta.ta_llegada_en_orden = args["ta_llegada_en_orden"]
        tipo_apuesta.ta_limite_premiado_inferior = args["ta_limite_premiado_inferior"]
        tipo_apuesta.ta_limite_premiado_superior = args["ta_limite_premiado_superior"]
        tipo_apuesta.ta_descripcion = args["ta_descripcion"]

        try:
            db.session.commit()
            return tipo_apuesta_schema.dumps(tipo_apuesta), 201
        except:
            db.session.rollback()
            return 'Could not be updated', 400
# add the endpoint ot the api
api.add_resource(TipoApuestaEndPoint, '/tipos/apuesta/<tipo_apuesta_id>')

# list all jinetes and create one
class TipoApuestaList(Resource):
    def get(self):
        tipos_apuestas = TipoApuesta.query.all()
        return [tipo_apuesta_schema.dumps(tipo_apuesta) for tipo_apuesta in tipos_apuestas]

    def post(self):
        try:
            args = tipo_apuesta_parser.parse_args()
            tipo_apuesta = TipoApuesta.create(**args)

            return tipo_apuesta_schema.dumps(tipo_apuesta), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(TipoApuestaList, '/tipos/apuesta')


### Color ###
# shows a list of all colors, and lets you POST to add new colors
class ColorListEndPoint(Resource):
    def get(self):
        colors = Color.query.all()
        return [color_schema.dump(color) for color in colors]

    def post(self):
        try:
            args = color_parser.parse_args()
            color = Color.create(**args)
            return color_schema.dump(color), 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(ColorListEndPoint, '/colors')

### Report ###
# generate a report
class ReportsEndPoint(Resource):
    def post(self):
        try:
            args = report_parser.parse_args()
            # get data
            file_name = args["file_name"]
            db_table = args["db_table"]

            generateReport(file_name, db_table)

            return 'Report generated', 201
        except BaseException as e:
            print(e)
            return 'Failed', 400
# add the endpoint ot the api
api.add_resource(ReportsEndPoint, '/reports')

#------------------------------------------------------------------------------------------

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
