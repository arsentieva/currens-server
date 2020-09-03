from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.Integer) # 1 = Male  and 2= Female
    weight = db.Column(db.Float)
    age = db.Column(db.Integer)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User: {self.name}, {self.lastname}, {self.email}'

    # TODO create to dictionary method
    def to_dictionary(self):
        return {
            "name": self.name,
            "lastname": self.lastname,
            "image_url": self.image_url,
            "email": self.email,
            "gender": self.gender,
            "weight": self.weight,
            "age": self.age,
        }


class Activity(db.Model):
    __tablename__="activities"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(50))
    pace = db.Column(db.Float)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    calories = db.Column(db.Integer)
    elevation_gain = db.Column(db.Integer)
    elevation_loss = db.Column(db.Integer)
    distance = db.Column(db.Float)
    heart_rate = db.Column(db.Integer)
    effort_level = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='activity', lazy=True)

    def to_dictionary(self):
        duration = self.end_time - self.start_time
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "pace": self.pace,
            "duration": json.dumps(duration.total_seconds().__str__()),
            "calories": self.calories,
            "date": json.dumps(self.start_time.__str__()),
            "elevation_gain": self.elevation_gain,
            "elevation_loss": self.elevation_loss,
            "distance": self.distance,
            "heart_rate": self.heart_rate,
            "effort_level": self.effort_level,
            "route": [route.to_dictionary() for route in self.route]
        }


class Route(db.Model):
    __tablename__="routes"

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    run = db.relationship("Activity", backref='route', lazy=True)

    def __repr__(self):
        return f'<Route {self.lat} - {self.lng}>'

    def to_dictionary(self):
        return{
            "lat":self.lat,
            "lng":self.lng,
        }
