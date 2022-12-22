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
# Color -----------------------------------------------------------------------------------
color_parser = reqparse.RequestParser()
color_parser.add_argument('col_nombre')

# schemas for the models ------------------------------------------------------------------

class ColorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Color
        include_fk = True
# instance the class
color_schema = ColorSchema()

#------------------------------------------------------------------------------------------

# endpoints -------------------------------------------------------------------------------

# Color
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
