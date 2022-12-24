"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import *

# marshmellow import
from flask_marshmallow import Marshmallow 
# flask-restful import
from flask_restful import reqparse, abort, Resource, Api
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
# Color -----------------------------------------------------------------------------------
color_parser = reqparse.RequestParser()
color_parser.add_argument('col_nombre')

# schemas for the models ------------------------------------------------------------------

# Ejemplar schema
class EjemplarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ejemplar
        include_fk = True
        json_module = simplejson
# instance the class
ejemplar_schema = EjemplarSchema()

# Entrenador schema
class EntrenadorSchema(ma.SQLAlchemyAutoSchema):
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

# Carrera schema
class CarreraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Carrera
        include_fk = True
        json_module = simplejson
# instance the class
carrera_schema = CarreraSchema()

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
        model = AccionTipoUsuario
        include_fk = True
        json_module = simplejson
# instance the class
usuario_schema = UsuarioSchema()

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
    except:
        db.session.rollback()
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
        carrera = Carrera.query.get(carrera_id)
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
api.add_resource(AccionTipoUsuarioEndPoint, '/accion-tipos-usuarios/<accion_tipo_usuario_id>')

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
api.add_resource(AccionTipoUsuarioListEndPoint, '/accion-tipos-usuarios')


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
