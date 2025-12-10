from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .. import db
from ..models import User

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.password_hash or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "credenciales inválidas"}), 401

    access_token = create_access_token(identity=str(user.id))
    # 🚨 ACTUALIZACIÓN: Incluir 'name' en la respuesta del Login
    return jsonify({
        "access_token": access_token, 
        "user": {
            "id": user.id, 
            "email": user.email,
            "name": user.name, 
            "is_member": user.is_member if hasattr(user, 'is_member') else False
        }
    }), 200

@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """Ruta para obtener los datos básicos del usuario actual a partir del token JWT."""
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    # 🚨 ACTUALIZACIÓN: Incluir 'name' en la respuesta de /me
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name, # <-- Nuevo campo añadido
        "is_member": user.is_member
    }), 200
    
@bp.route("/register", methods=["POST"])
def register():
    """Ruta para registrar un nuevo usuario con email, nombre y contraseña."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name") # ⬅️ Usamos el campo 'name'

    # 1. Validación de campos
    if not email or not password or not name:
        return jsonify({"msg": "Faltan campos requeridos (email, password, name)"}), 400

    # 2. Verificar si el usuario ya existe
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "El email ya está registrado"}), 409 # Conflict

    # 3. Hashear la contraseña por seguridad
    hashed_password = generate_password_hash(password)

    # 4. Crear el nuevo usuario (este código ya estaba correcto)
    new_user = User(
        email=email,
        name=name,
        password_hash=hashed_password
    )

    # 5. Guardar en la base de datos
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar usuario: {e}")
        return jsonify({"msg": "Error al guardar el usuario en la base de datos"}), 500

    # 6. Responder con éxito
    return jsonify({"msg": "Registro exitoso", "user_id": new_user.id}), 201