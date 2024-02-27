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
from models import db, Users, Films, Characters, Species, Planets


# Istancias de Flask
app = Flask(__name__)
app.url_map.strict_slashes = False
# Configuracion de DB
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


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route("/users", methods=["GET", "POST"])
def handle_users():
    response_body = results = {}
    if request.method == "GET":
        users = db.session.execute(db.select(Users)).scalars()
        response_body["results"] = [row.serialize() for row in users]
        response_body["message"] = "Metodo GET de users"
        return response_body, 200
    if request.method == "POST":
        data = request.json
        user = Users( 
            password = data["password"],
            email = data["email"],
            is_active = True)
        db.session.add(user)
        db.session.commit()
        response_body["message"] = "Metodo POST de users"
        response_body["result"] = user.serialize()
        return response_body, 200


@app.route("/planets", methods=["GET", "POST"])
def handle_planets():
    response_body = {}
    if request.method == "GET":
        planets = db.session.execute(db.select(Planets)).scalars()
        response_body["message"] = "Planets List"
        response_body["results"] = [row.serialize() for row in planets]
        return response_body, 200
    if request.method == "POST":
        data = request.json
        planet = Planets(name = data["name"])
        db.session.add(planet)
        db.session.commit()
        response_body["message"] = "Planet added"
        response_body["result"] = planet.serialize()
        return response_body, 200


@app.route("/characters", methods=["GET", "POST"])
def handle_characters():
    if request.method == "GET":
        response_body = {}
        characters = db.session.execute(db.select(Characters)).scalars()
        response_body["message"] = "Characters List"
        response_body["results"] = [row.serialize() for row in characters]
        return response_body, 200
    if request.method == "POST":
        data = request.json
        character = Characters(name = data["name"])
        db.session.add(character)
        db.session.commit()
        response_body["message"] = "Character added"
        response_body["result"] = character.serialize()
        return response_body, 200


@app.route("/films", methods=["GET", "POST"])
def handle_films():
    response_body = {}
    if request.method == "GET":
        films = db.session.execute(db.select(Films)).scalars()
        response_body["message"] = "Films List"
        response_body["results"] = [row.serialize() for row in films]
        return response_body, 200
    if request.method == "POST":
        data = request.json
        film = Films(name = data["name"])
        db.session.add(film)
        db.session.commit()
        response_body["message"] = "Film added"
        response_body["result"] = film.serialize()
        return response_body, 200


@app.route("/species", methods=["GET", "POST"])
def handle_species():
    response_body = {}
    if request.method == "GET":
        species = db.session.execute(db.select(Species)).scalars()
        response_body["message"] = "Species List"
        response_body["results"] = [row.serialize() for row in species]
        return response_body, 200
    if request.method == "POST":
        data = request.json
        specie = Species(name = data["name"])
        db.session.add(specie)
        db.session.commit()
        response_body["message"] = "Specie added"
        response_body["result"] = specie.serialize()
        return response_body, 200 


@app.route("/users/<int:id>", methods=["GET", "DELETE", "PATCH"])
def handle_user(id):
    response_body = {}
    user = db.session.get(Users, id)
    if request.method == "GET":
        if user:
            response_body["message"] = "Metodo GET de users"
            response_body["result"] = user.serialize()
            return response_body, 200
        else:
            response_body["message"] = "User not found"
            return response_body, 404
    if request.method == "DELETE":
        if user:
            db.session.delete(user)
            db.session.commit()
            response_body["message"] = "User delete"
            response_body["user delete"] = user.serialize()
            return response_body, 200
        else:
            response_body["message"] = "User not found"
            return response_body, 404
    if request.method == "PATCH":
        if user:
            data = request.json
            if 'email' in data:
                user.email = data["email"]
            if 'password' in data:
                user.password = data["password"]
            db.session.add(user)
            db.session.commit()
            response_body["message"] = "User update"
            response_body["result"] = user.serialize()
            return response_body, 200
        else:
            response_body["message"] = "User not found"
            return response_body, 404


@app.route("/planets/<int:id>", methods=["GET", "DELETE", "PUT"])
def handle_planet(id):
    response_body = {}
    planet = db.session.get(Planets, id)
    if request.method == "GET":
        if planet:
            response_body["message"] = "Metodo GET de planets"
            response_body["result"] = planet.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Planet not found"
            return response_body, 404
    if request.method == "DELETE":
        if planet:
            db.session.delete(planet)
            db.session.commit()
            response_body["message"] = "Planet delete"
            response_body["planet delete"] = planet.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Planet not found"
            return response_body, 404
    if request.method == "PUT":
        if planet:
            data = request.json
            planet.name = data["name"]
            db.session.add(planet)
            db.session.commit()
            response_body["message"] = "Planet update"
            response_body["result"] = planet.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Planet not found"
            return response_body, 404
        

@app.route("/characters/<int:id>", methods=["GET", "DELETE", "PUT"])
def handle_character(id):
    response_body = {}
    character = db.session.get(Characters, id)
    if request.method == "GET":
        if characters:
            response_body["message"] = "Metodo GET de characters"
            response_body["result"] = character.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Character not found"
            return response_body, 404
    if request.method == "DELETE":
        if characters:
            db.session.delete(character)
            db.session.commit()
            response_body["message"] = "Character delete"
            response_body["character delete"] = character.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Character not found"
            return response_body, 404
    if request.method == "PUT":
        if character:
            data = request.json
            character.name = data["name"]
            db.session.add(character)
            db.session.commit()
            response_body["message"] = "Character update"
            response_body["result"] = character.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Character not found"
            return response_body, 404
        

@app.route("/films/<int:id>", methods=["GET", "DELETE", "PUT"])
def handle_film(id):
    response_body = {}
    film = db.session.get(Films, id)
    if request.method == "GET":
        if film:
            response_body["message"] = "Metodo GET de films"
            response_body["result"] = film.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Film not found"
            return response_body, 404
    if request.method == "DELETE":
        if film:
            db.session.delete(film)
            db.session.commit()
            response_body["message"] = "Character delete"
            response_body["film delete"] = film.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Film not found"
            return response_body, 404
    if request.method == "PUT":
        if film:
            data = request.json
            film.name = data["name"]
            db.session.add(film)
            db.session.commit()
            response_body["message"] = "Film update"
            response_body["result"] = film.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Film not found"
            return response_body, 404


@app.route("/species/<int:id>", methods=["GET", "DELETE", "PUT"])
def handle_specie(id):
    response_body = {}
    specie = db.session.get(Species, id)
    if request.method == "GET":
        if specie:
            response_body["message"] = "Metodo GET de species"
            response_body["result"] = specie.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Specie not found"
            return response_body, 404 
    if request.method == "DELETE":
        if specie:
            db.session.delete(specie)
            db.session.commit()
            response_body["message"] = "Specie delete"
            response_body["planet delete"] = specie.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Specie not found"
            return response_body, 404
    if request.method == "PUT":
        if specie:
            data = request.json
            specie.name = data["name"]
            db.session.add(specie)
            db.session.commit()
            response_body["message"] = "Specie update"
            response_body["result"] = specie.serialize()
            return response_body, 200
        else:
            response_body["message"] = "Specie not found"
            return response_body, 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
