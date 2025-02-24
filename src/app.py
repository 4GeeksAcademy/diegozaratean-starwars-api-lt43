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
from models import db, User, Empresa
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# INICIO DEL CODIGO

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    print('get all users')
    user = User.query.get(1)
    print(user)
    print(user.serialize())

    all_users = User.query.all()
    print(all_users)
    results = list(map(lambda user: user.serialize(),all_users))
    print(results)
    


    response_body = {
        "msg": "lista de todos los usuairos ",
        "users": results
    }

    return jsonify(response_body), 200

@app.route('/test', methods=['GET'])
def test():

    response_body = {
        "msg": "esto esw una prueba  "
    }

    return jsonify(response_body), 200

@app.route('/empresa', methods=['GET'])
def get_empresas():
    all_companies = Empresa.query.all()
    results = list(map(lambda company: company.serialize(),all_companies))

    return jsonify(results), 200


@app.route('/empresa/<int:company_id>', methods=['GET'])
def get_compnay(company_id):
    company = Empresa.query.get(company_id)
    return jsonify(company.serialize()), 200



# FIN DEL CODIGO


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
