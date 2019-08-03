from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "planets.db")}'

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(name='Mercury', type='Class D', home_star='Sol', mass=3.258e23, radius=1516, distance=35.98e6)
    venus = Planet(name='Venus', type='Class K', home_star='Sol', mass=4.867e24, radius=3760, distance=67.24e6)
    earth = Planet(name='Earth', type='Class M', home_star='Sol', mass=5.972e24, radius=3959, distance=92.96e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='William', last_name='Herschel', email='test@test.com', password='12345')

    db.session.add(test_user)

    db.session.commit()
    print('Database seeded!')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API.')


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = request.args.get('age', type=int)

    if age < 18:
        return jsonify(message=f'Sorry {name} you are not old enough.'), 401
    else:
        return jsonify(message=f'Welcome {name} you are old enough!')


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message=f'Sorry {name} you are not old enough.'), 401
    else:
        return jsonify(message=f'Welcome {name} you are old enough!')


@app.route('/planets', methods=['GET'])
def planets():
    planets = Planet.query.all()
    result = planets_schema.dump(planets)

    return jsonify(result.data)


# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'type', 'home_star', 'mass', 'radius', 'distance')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

if __name__ == '__main__':
    app.run()
