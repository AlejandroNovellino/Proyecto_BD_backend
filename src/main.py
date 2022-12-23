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
            abort(404, message="Entrenador {} doesn't exist".format(jinete_id))

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
        #update the Ejemplar
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

# list all entrenadores and create one
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
