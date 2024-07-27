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
from models import db, User, People, Planet, Vehicle
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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    users = db.session.execute(db.select(User).order_by(User.email)).scalars()
    user_list = [user.serialize() for user in users]
    response_body = {
        "msg": " User List ",
        "results": user_list}

    return jsonify(response_body), 200

@app.route('/user/favorites', methods=['GET'])
def get_all_favorites():
    user_id = request.json['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        response_body = {
            "msg": "This user was not found"}
        return jsonify(response_body), 404
    favorites = {
        "planets": [x.serialize() for x in user.favorite_planets],
        "people": [x.serialize() for x in user.favorite_people],
        "vehicles": [x.serialize() for x in user.favorite_vehicles],
    }
    response_body = {
        "msg": "These are your favorites",
        "favorites": favorites
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = db.session.execute(db.select(People).order_by(People.name)).scalars()
    people_list = [person.serialize() for person in people]
    response_body = {
        "msg": " People List ",
        "results": people_list}
    
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id): 
    person = People.query.filter_by(id=people_id).first()
    if person is None:
        response_body = {
        "msg": " This person does not exist "}
        return jsonify(response_body), 404
    response_body = {
        "msg": " Here is your person ",
        "result": person.serialize()}
    return jsonify(response_body), 200

@app.route('/favorites/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "This user was not found"}), 404
    
    person = People.query.filter_by(id=people_id).first()
    if person is None:
        return jsonify({"msg": "This person was not found"}), 404
    
    if user.favorite_people is None:
        user.favorite_people = []

    if person in user.favorite_people:
        return jsonify({"msg": "This person already in favorites"}), 409
    user.favorite_people.append(person)
    response_body = {
        "msg": " Here are your favorite people ",
        "result": [x.serialize() for x in user.favorite_people]
    }
    return jsonify(response_body), 201

@app.route('/planets', methods=['GET'])
def get_planets():
    planet = db.session.execute(db.select(Planet).order_by(Planet.name)).scalars()
    planets_list = [planet.serialize() for planet in planet]
    response_body = {
        "msg": " Planet List ",
        "results": planets_list
    }

    return jsonify(response_body), 200

@app.route('/favorites/planets/<int:planets_id>', methods=['POST'])
def add_favorite_planets(planets_id):
    user_id = request.json['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "This user was not found"}), 404
    
    planets = planets.query.filter_by(id=planets_id).first()
    if planets is None:
        return jsonify({"msg": "This planet was not found"}), 404
    
    if user.favorite_planets is None:
        user.favorite_planets = []

    if planets in user.favorite_planets:
        return jsonify({"msg": "This planet is already in favorites"}), 409
    user.favorite_planets.append(planets)
    response_body = {
        "msg": " Here are your favorite planets ",
        "result": [x.serialize() for x in user.favorite_planets]
    }
    return jsonify(response_body), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
