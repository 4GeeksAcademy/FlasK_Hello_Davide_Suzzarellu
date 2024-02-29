from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User: {self.id} - Email: {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
        }


class Films(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Film: {self.id} - Name: {self.name}>' 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }     


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Character: {self.id} - Name: {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }  


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Planet: {self.id} - Name: {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }   


class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Specie: {self.id} - Name: {self.name}>' 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }  


class FavouritesFilms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users", foreign_keys=[user_id])
    film_id = db.Column(db.Integer, db.ForeignKey("films.id"))
    film = db.relationship("Films", foreign_keys=[film_id])

    def __repr__(self):
        return f'<Favourite: {self.id} - User: {self.user_id} - Film: {self.film_id}>' 

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "film": self.film_id
        } 


class FavouritesPlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users", foreign_keys=[user_id])
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    planet = db.relationship("Planets", foreign_keys=[planet_id])

    def __repr__(self):
        return f'<Favourite: {self.id} - User: {self.user_id} - Planet: {self.planet_id}>' 

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "planet": self.planet_id
        } 


class FavouritesCharacters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users", foreign_keys=[user_id])
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    character = db.relationship("Characters", foreign_keys=[character_id])

    def __repr__(self):
        return f'<Favourite: {self.id} - User: {self.user_id} - Character: {self.character_id}>' 

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "character": self.character_id
        }   


class FavouritesSpecies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users", foreign_keys=[user_id])
    specie_id = db.Column(db.Integer, db.ForeignKey("species.id"))
    specie = db.relationship("Species", foreign_keys=[specie_id])

    def __repr__(self):
        return f'<Favourite: {self.id} - User: {self.user_id} - Specie: {self.specie_id}>' 

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "specie": self.specie_id
        }   


class Favourites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users", foreign_keys=[user_id])
    film_id = db.Column(db.Integer, db.ForeignKey("films.id"))
    film = db.relationship("Films", foreign_keys=[film_id])
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    planet = db.relationship("Planets", foreign_keys=[planet_id])
    specie_id = db.Column(db.Integer, db.ForeignKey("species.id"))
    specie = db.relationship("Species", foreign_keys=[specie_id])
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    character = db.relationship("Characters", foreign_keys=[character_id])

    def __repr__(self):
        return f'<Favourites {self.id} - {self.user_id} - {self.film_id} - {self.planet_id} - {self.specie_id} - {self.character_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "film": self.film,
            "planet": self.planet,
            "species": self.specie,
            "characters": self.character
        }

