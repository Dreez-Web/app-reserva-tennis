from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Court
from .. import db

bp = Blueprint("admin", __name__)

def require_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == "admin"

@bp.route("/courts", methods=["POST"])
@jwt_required()
def create_court():
    user_id = get_jwt_identity()
    if not require_admin(user_id):
        return jsonify({"msg": "no autorizado"}), 403

    data = request.get_json()
    name = data.get("name")
    sport = data.get("sport", "tennis")
    price_member = data.get("price_member", 10.0)
    price_guest = data.get("price_guest", 20.0)

    court = Court(name=name, sport=sport, price_member=price_member, price_guest=price_guest)
    db.session.add(court)
    db.session.commit()
    return jsonify({"msg": "cancha creada", "court_id": court.id}), 201
