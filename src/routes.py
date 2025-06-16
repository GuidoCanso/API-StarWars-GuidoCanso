from flask import Blueprint, request, jsonify
from models import db, People, Planet, User, Favorite

api = Blueprint('api', __name__)

# GET /people - Lista todos los personajes
@api.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([p.to_dict() for p in people]), 200

# GET /people/<int:id> - Detalle de personaje
@api.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    person = People.query.get(id)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.to_dict()), 200

# GET /planets - Lista todos los planetas
@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200

# GET /planets/<int:id> - Detalle de planeta
@api.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# GET /users - Lista usuarios
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

# GET /users/<int:id> - Detalle usuario
@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

# GET /favorites/user/<int:user_id> - Favoritos de un usuario
@api.route('/favorites/user/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([f.serialize() for f in favorites]), 200

# POST /favorites - Crear favorito
@api.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    user_id = data.get('user_id')
    people_id = data.get('people_id')
    planet_id = data.get('planet_id')

    if not user_id or (not people_id and not planet_id):
        return jsonify({"error": "user_id and one of people_id or planet_id are required"}), 400

    favorite = Favorite(user_id=user_id, people_id=people_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201
