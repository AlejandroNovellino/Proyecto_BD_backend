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
