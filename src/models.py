from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_people = db.Table(
    "favorite_people",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("person_id", db.ForeignKey("people.id")),
)

favorite_planets = db.Table(
    "favorite_planets",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("planet_id", db.ForeignKey("planet.id")),
)

favorite_vehicles = db.Table(
    "favorite_vehicles",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("vehicle_id", db.ForeignKey("vehicle.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_people = db.relationship('People', secondary=favorite_people)
    favorite_planets = db.relationship('Planet', secondary=favorite_planets)
    favorite_vehicles = db.relationship('Vehicle', secondary=favorite_vehicles)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_people": [x.serialize() for x in self.favorite_people],
            "favorite_planets": [x.serialize() for x in self.favorite_planets],
            "favorite_vehicles": [x.serialize() for x in self.favorite_vehicles]
            # do not serialize the password, its a security breach
        }
    
#serialize people

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=True)
    mass = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    birth_year = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    
    


    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "created": self.created,
            "edited": self.edited,
            "description": self.description,
            
        }
    
# serialize planets

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(250), nullable=False)
    edited = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)


    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created,
            "edited": self.edited,
            "description": self.description
            
        }
    
# serialize vehicles

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    vehicle_class = db.Column(db.String(250), nullable=True)
    manufacturer = db.Column(db.String(250), nullable=True)
    cost_in_credits = db.Column(db.String(250), nullable=True)
    length = db.Column(db.String(250), nullable=True)
    crew = db.Column(db.String(250), nullable=True)
    passengers = db.Column(db.String(250), nullable=True)
    max_atmosphering_speed = db.Column(db.String(250), nullable=True)
    cargo_capacity = db.Column(db.String(250), nullable=True)
    consumables = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)


    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew ": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "created": self.created,
            "edited": self.edited,
            "description": self.description,

        }