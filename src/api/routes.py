from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from sqlalchemy import select

api = Blueprint('api', __name__)

# -----------------------------
# LOGIN: Genera JWT
# -----------------------------
@api.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = db.session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"msg": "Contraseña incorrecta"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

# -----------------------------
# CREAR USUARIO (protegido)
# -----------------------------
@api.route('/usuario', methods=["POST"])
@jwt_required()
def crear_usuario():
    data = request.get_json()
    current_user_id = int(get_jwt_identity())

    # Solo usuarios existentes pueden crear nuevos usuarios
    user = db.session.get(User, current_user_id)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    # Verifica si ya existe un usuario con ese email
    if db.session.execute(select(User).where(User.email == data.get("email"))).scalar_one_or_none():
        return jsonify({"msg": "El email ya está registrado"}), 409

    nuevo_usuario = User(
        email=data.get("email"),
        password=generate_password_hash(data.get("password")),
        is_active=True
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "msg": "Usuario creado correctamente",
        "usuario": nuevo_usuario.serialize()
    }), 200

# -----------------------------
# ELIMINAR USUARIO (protegido)
# -----------------------------
@api.route('/usuario/<int:usuario_id>', methods=["DELETE"])
@jwt_required()
def eliminar_usuario(usuario_id):
    current_user_id = int(get_jwt_identity())
    user = db.session.get(User, current_user_id)

    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    # Evita que el usuario se elimine a sí mismo
    if user.id == usuario_id:
        return jsonify({"msg": "No puedes eliminar tu propio usuario"}), 405

    usuario = db.session.execute(select(User).where(User.id == usuario_id)).scalar_one_or_none()
    if usuario is None:
        return jsonify({"msg": "Usuario a eliminar no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"msg": "Usuario eliminado correctamente"}), 200
