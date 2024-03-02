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
from models import db, Users, Films, Characters, Species, Planets, FavouritesFilms, FavouritesPlanets, FavouritesCharacters, FavouritesSpecies, Favourites


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


@app.route("/users/<int:id>/favourites/films", methods=["GET", "POST"])
def handle_favourites_films(id):
    response_body = {}
    user = db.session.get(Users, id)
    favourite_films = (
        db.session.query(Films)
        .join(FavouritesFilms, FavouritesFilms.film_id == Films.id)
        .filter(FavouritesFilms.user_id == user.id if user else None)
        .all()
    )
    if not user:
        response_body["message"] = "User not found"
        return response_body, 404
    else:
        if request.method == "GET":
            if favourite_films:
                response_body["message"] = "Favourites films"
                response_body["result"] = {
                        "user_id": user.id,
                        "email": user.email,
                        "favourite_films": [film.serialize() for film in favourite_films]
                    }
                return response_body, 200
            else:
                response_body["message"] = "Error: User have no favourites films"
                return response_body, 404
        if request.method == "POST":
            data = request.json
            if "film_id" not in data:
                response_body["message"] = "Error: insert the Film ID"
                return response_body, 400
            else:
                film_id = data["film_id"]
            existing_film = Films.query.get(film_id)
            if not existing_film:
                response_body["message"] = f"Error: film with ID {film_id} does no exist"
                return response_body, 404
            existing_favourite_film = FavouritesFilms.query.filter_by(user_id=user.id, film_id=film_id).first()
            if existing_favourite_film:
                response_body["message"] = "The film is already in the favourites"
                return response_body, 400
            else:
                new_favourite_film = FavouritesFilms(user_id=user.id, film_id=film_id)
                db.session.add(new_favourite_film)
                db.session.commit()
                response_body["message"] = "Film added in a favourites list"
                response_body["result"] = {
                    "email": user.email,
                    "favourite_film": new_favourite_film.film.serialize()
                }
        return response_body, 201


@app.route("/users/<int:id>/favourites/planets", methods=["GET", "POST"])
def handle_favourites_planets(id):
    response_body = {}
    user = Users.query.get(id)
    favourites_planets = (
        db.session.query(Planets)
        .join(FavouritesPlanets, FavouritesPlanets.planet_id == Planets.id)
        .filter(FavouritesPlanets.user_id == user.id if user else None)
        .all()
    )
    if not user:
        response_body["message"] = "User not found"
        return response_body, 404
    else:
        if request.method == "GET":
            if favourites_planets:
                response_body["message"] = "Favourites planets"
                response_body["result"] = {
                        "user_id": user.id,
                        "email": user.email,
                        "favourites_planets": [planet.serialize() for planet in favourites_planets]
                    }
                return response_body, 200
            else:
                response_body["message"] = "Error: User have no favourites planets"
                return response_body, 404
        if request.method == "POST":
            data = request.json
            if "planet_id" not in data:
                response_body["message"] = "Error: insert the Planet ID"
                return response_body, 400
            else:
                planet_id = data["planet_id"]
            existing_planet = Planets.query.get(planet_id)
            if not existing_planet:
                response_body["message"] = f"Error: planet with ID {planet_id} does  no exist"
                return response_body, 404
            existing_favourite_planet = FavouritesPlanets.query.filter_by(user_id=user.id, planet_id=planet_id).first()
            if existing_favourite_planet:
                response_body["message"] = "The planet is already in the favourites"
                return response_body, 400
            else:
                new_favourite_planet = FavouritesPlanets(user_id=user.id, planet_id=planet_id)
                db.session.add(new_favourite_planet)
                db.session.commit()
                response_body["message"] = "Planets added in a favourites list"
                response_body["result"] = {
                    "user_id": user.id,
                    "email": user.email,
                    "favourite_planet": new_favourite_planet.planet.serialize()
                }
        return response_body, 201


@app.route("/users/<int:id>/favourites/species", methods=["GET", "POST"])
def handle_favourites_species(id):
    response_body = {}
    user = db.session.get(Users, id)
    favourite_species = (
        db.session.query(Species)
        .join(FavouritesSpecies, FavouritesSpecies.specie_id == Species.id)
        .filter(FavouritesSpecies.user_id == user.id)
        .all()
    )
    if not user:
        response_body["message"] = "User not found"
        return response_body, 404
    else:
        if request.method == "GET":
            if favourite_species:
                response_body["message"] = "Favourites species"
                response_body["result"] = {
                        "user_id": user.id,
                        "email": user.email,
                        "favourite_species": [specie.serialize() for specie in favourite_species]
                    }
                return response_body, 200
            else:
                response_body["message"] = "Error: User have no favourites species"
                return response_body, 404
        if request.method == "POST":
            data = request.json
            if "specie_id" not in data:
                response_body["message"] = "Error: insert the Specie ID"
                return response_body, 400
            else:
                specie_id = data["specie_id"]
            existing_specie = Species.query.get(specie_id)
            if not existing_specie:
                response_body["message"] = f"Error: specie with ID {specie_id} does no exist"
                return response_body, 404
            existing_favourite_specie = FavouritesSpecies.query.filter_by(user_id=user.id, specie_id=specie_id).first()
            if existing_favourite_specie:
                response_body["message"] = "The specie is already in the favourites"
                return response_body, 400
            else:
                new_favourite_specie = FavouritesSpecies(user_id=user.id, specie_id=specie_id)
                db.session.add(new_favourite_specie)
                db.session.commit()
                response_body["message"] = "Specie added in a favourites list"
                response_body["result"] = {
                    "email": user.email,
                    "favourite_specie": new_favourite_specie.specie.serialize()
                }
        return response_body, 201


@app.route("/users/<int:id>/favourites/characters", methods=["GET", "POST"])
def handle_favourites_characters(id):
    response_body = {}
    user = db.session.get(Users, id)
    favourite_characters = (
        db.session.query(Characters)
        .join(FavouritesCharacters, FavouritesCharacters.character_id == Characters.id)
        .filter(FavouritesCharacters.user_id == user.id if user else None)
        .all()
    )
    if not user:
        response_body["message"] = "User not found"
        return response_body, 404
    else:
        if request.method == "GET":
            if favourite_characters:
                response_body["message"] = "Favourites characters"
                response_body["result"] = {
                        "user_id": user.id,
                        "email": user.email,
                        "favourite_characters": [character.serialize() for character in favourite_characters]
                    }
                return response_body, 200
            else:
                response_body["message"] = "Error: User have no favourites characters"
                return response_body, 404
        if request.method == "POST":
            data = request.json
            if "character_id" not in data:
                response_body["message"] = "Error: insert the character ID"
                return response_body, 400
            else:
                character_id = data["character_id"]
            existing_character = Characters.query.get(character_id)
            if not existing_character:
                response_body["message"] = f"Error: character with ID {character_id} does no exist"
                return response_body, 404
            existing_favourite_character = FavouritesCharacters.query.filter_by(user_id=user.id, character_id=character_id).first()
            if existing_favourite_character:
                response_body["message"] = "The character is already in the favourites"
                return response_body, 400
            else:
                new_favourite_character = FavouritesCharacters(user_id=user.id, character_id=character_id)
                db.session.add(new_favourite_character)
                db.session.commit()
                response_body["message"] = "Character added in a favourites list"
                response_body["result"] = {
                    "email": user.email,
                    "favourite_character": new_favourite_character.character.serialize()
                }
        return response_body, 201

    
@app.route("/users/<int:id>/favourites")
def handle_user_favourites(id):
    response_body = {}
    user = Users.query.get(id)
    if not user:
        response_body["message"] = "User not found"
        return jsonify(response_body), 404
    favourite_characters = (
        db.session.query(Characters)
        .join(FavouritesCharacters, FavouritesCharacters.character_id == Characters.id)
        .filter(FavouritesCharacters.user_id == user.id if user else None)
        .all()
    )
    favourite_species = (
        db.session.query(Species)
        .join(FavouritesSpecies, FavouritesSpecies.specie_id == Species.id)
        .filter(FavouritesSpecies.user_id == user.id if user else None)
        .all()
    )
    favourites_planets = (
        db.session.query(Planets)
        .join(FavouritesPlanets, FavouritesPlanets.planet_id == Planets.id)
        .filter(FavouritesPlanets.user_id == user.id if user else None)
        .all()
    )
    favourite_films = (
        db.session.query(Films)
        .join(FavouritesFilms, FavouritesFilms.film_id == Films.id)
        .filter(FavouritesFilms.user_id == user.id if user else None)
        .all()
    )
    response_body["message"] = "User's favourites"
    response_body["result"] = {
        "characters": [character.serialize() for character in favourite_characters],
        "species": [specie.serialize() for specie in favourite_species],
        "planets": [planet.serialize() for planet in favourites_planets],
        "films": [film.serialize() for film in favourite_films],
    }
    if not (favourite_characters or favourite_species or favourites_planets or favourite_films):
        response_body["message"] = "User have no favorites"
        return jsonify(response_body), 404
    response_body["message"] = "User's favourites"
    response_body["result"] = {
        "characters": [character.serialize() for character in favourite_characters],
        "species": [specie.serialize() for specie in favourite_species],
        "planets": [planet.serialize() for planet in favourites_planets],
        "films": [film.serialize() for film in favourite_films],
    }

    return jsonify(response_body), 200


@app.route("/users/<int:id>/favourites/films/<int:film_id>", methods=["DELETE", "GET"])
def handle_delete_favourites_film(id, film_id):
    response_body = {}
    user = db.session.query(Users).get(id)
    if not user:
        response_body["message"] = "Error: User not found"
        return response_body, 404
    else:
        if request.method == "DELETE":
            favourite_film = (
                db.session.query(FavouritesFilms)
                .filter_by(user_id=user.id, film_id=film_id)
                .first()
            )
            if favourite_film:
                db.session.delete(favourite_film)
                db.session.commit()
                user_favourite_films = (
                    db.session.query(Films)
                    .join(FavouritesFilms, FavouritesFilms.film_id == Films.id)
                    .filter(FavouritesFilms.user_id == user.id)
                    .all()
                )
                response_body["message"] = "Film removed from favorites"
                response_body["result"] = {
                    "user_id": user.id,
                    "email": user.email,
                    "favourite_films": [film.serialize() for film in user_favourite_films]
                }
                return response_body, 200
            else:
                response_body["message"] = "Error: Film not found in user's favorites"
                return response_body, 404
        if request.method == "GET":
            favourite_film = (
                db.session.query(FavouritesFilms)
                .filter_by(user_id=user.id, film_id=film_id)
                .first()
            )
            if favourite_film:
                response_body["message"] = f'Favourite film, with id: {film_id}'
                response_body["result"] = favourite_film.serialize()
                return response_body, 200
                print(response_body)
            else:
                response_body["message"] = "Film not found"
                return response_body, 400


@app.route("/users/<int:id>/favourites/planets/<int:planet_id>", methods=["DELETE", "GET"])
def handle_delete_favourites_planet(id, planet_id):
    response_body = {}
    user = db.session.query(Users).get(id)
    if not user:
        response_body["message"] = "Error: User not found"
        return response_body, 404
    else:
        if request.method == "DELETE":
            favourite_planet = (
                db.session.query(FavouritesPlanets)
                .filter_by(user_id=user.id, planet_id=planet_id)
                .first()
            )
            if favourite_planet:
                db.session.delete(favourite_planet)
                db.session.commit()
                user_favourite_planets = (
                    db.session.query(Planets)
                    .join(FavouritesPlanets, FavouritesPlanets.planet_id == Planets.id)
                    .filter(FavouritesPlanets.user_id == user.id)
                    .all()
                )
                response_body["message"] = "Planet removed from favorites"
                response_body["result"] = {
                    "user_id": user.id,
                    "email": user.email,
                    "favourite_planet": [planet.serialize() for planet in user_favourite_planets]
                }
                return response_body, 200
            else:
                response_body["message"] = "Error: Planet not found in user's favorites"
                return response_body, 404
        if request.method == "GET":
            favourite_planet = (
                db.session.query(FavouritesPlanets)
                .filter_by(user_id=user.id, planet_id=planet_id)
                .first()
            )
            if favourite_planet:
                response_body["message"] = f'Planet with id: {planet_id}'
                response_body["result"] = favourite_planet.serialize()
                return response_body, 200
            else:
                response_body["message"] = "Planet not found"
                return response_body, 400


@app.route("/users/<int:id>/favourites/species/<int:specie_id>", methods=["DELETE", "GET"])
def handle_delete_favourites_specie(id, specie_id):
    response_body = {}
    user = db.session.query(Users).get(id)
    if not user:
        response_body["message"] = "Error: User not found"
        return response_body, 404
    else:
        if request.method == "DELETE":
            favourite_specie = (
                db.session.query(FavouritesSpecies)
                .filter_by(user_id=user.id, specie_id=specie_id)
                .first()
            )
            if favourite_specie:
                db.session.delete(favourite_specie)
                db.session.commit()
                user_favourite_species = (
                    db.session.query(Planets)
                    .join(FavouritesSpecies, FavouritesSpecies.specie_id == Species.id)
                    .filter(FavouritesSpecies.user_id == user.id)
                    .all()
                )
                response_body["message"] = "Species removed from favorites"
                response_body["result"] = {
                    "user_id": user.id,
                    "email": user.email,
                    "favourite_specie": [specie.serialize() for specie in user_favourite_species]
                }
                return response_body, 200
            else:
                response_body["message"] = "Error: Species not found in user's favorites"
                return response_body, 404
        if request.method == "GET":
            favourite_specie = (
                db.session.query(FavouritesSpecies)
                .filter_by(user_id=user.id, specie_id=specie_id)
                .first()
            )
            if favourite_specie:
                response_body["message"] = f'Specie with id: {specie_id}'
                response_body["result"] = favourite_specie.serialize()
                return response_body, 200
            else:
                response_body["message"] = "Specie not found"
                return response_body, 400
    

@app.route("/users/<int:id>/favourites/characters/<int:character_id>", methods=["DELETE", "GET"])
def handle_delete_favourites_character(id, character_id):
    response_body = {}
    user = db.session.query(Users).get(id)
    if not user:
        response_body["message"] = "Error: User not found"
        return response_body, 404
    else:
        if request.method == "DELETE":
            favourite_character = (
                db.session.query(FavouritesCharacters)
                .filter_by(user_id=user.id, character_id=character_id)
                .first()
            )
            if favourite_character:
                db.session.delete(favourite_character)
                db.session.commit()
                user_favourite_characters = (
                    db.session.query(Characters)
                    .join(FavouritesCharacters, FavouritesCharacters.character_id == Characters.id)
                    .filter(FavouritesCharacters.user_id == user.id)
                    .all()
                )
                response_body["message"] = "Characters removed from favorites"
                response_body["result"] = {
                    "user_id": user.id,
                    "email": user.email,
                    "favourite_character": [character.serialize() for character in user_favourite_characters]
                }
                return response_body, 200
            else:
                response_body["message"] = "Error: Characters not found in user's favorites"
                return response_body, 404
        if request.method == "GET":
            favourite_character = (
                db.session.query(FavouritesCharacters)
                .filter_by(user_id=user.id, character_id=character_id)
                .first()
            )
            if favourite_character:
                response_body["message"] = f'Character with id: {character_id}'
                response_body["result"] = favourite_character.serialize()
                return response_body, 200
            else:
                response_body["message"] = "Character not found"
                return response_body, 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
