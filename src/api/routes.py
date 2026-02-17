"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# CREAR TOKEN PARA INICIAR SESIÓN


@api.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = db.session.execute(select(User).where(
        User.email == email, User.password == password)).scalar_one_or_none()

    if user is None:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"token": access_token, "user_id": user.id}), 200
# CREAR USUARIO


@api.route('/usuario', methods=["POST"])
@jwt_required()
def crear_usuario():
    data = request.get_json()
    current_user_id = int(get_jwt_identity())

    user = db.session.get(User, current_user_id)

    if user is None:
        return ({"msg": "Usuario no encontrado"}), 404

    ##Creando mi nuevo usuario!!!!
    nuevo_usuario = User(
        email=data.get("email"),
        password=data.get("password"),
        is_active=True 
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "msg": "Usuario creado correctamente",
        "usuario": nuevo_usuario.serialize()
    }), 200

# ELIMINAR UN USUARIO


@api.route('/usuario/<int:usuario_id>', methods=["DELETE"])
@jwt_required()
def eliminar_usuario(usuario_id):
    current_user_id = int(get_jwt_identity())
    user = db.session.get(User, current_user_id)

    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    if user.id == usuario_id:
        return jsonify({"msg": "No puedes eliminar tu usuario"}), 405

    usuario = db.session.execute(select(User).where(
        User.id == usuario_id)).scalar_one_or_none()
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({
        "msg": "Usuario eliminado correctamente"
    }), 200