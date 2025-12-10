from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Booking, Court, User
from datetime import datetime
from decimal import Decimal

bp = Blueprint("bookings", __name__)

@bp.route("", methods=["GET"])
@jwt_required()
def my_bookings():
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id).all()
    result = []
    for b in bookings:
        result.append({
            "id": b.id,
            "court_id": b.court_id,
            "start": b.start_time.isoformat(),
            "end": b.end_time.isoformat(),
            "price": str(b.price)
        })
    return jsonify(result), 200

@bp.route("", methods=["POST"])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    court_id = data.get("court_id")
    start_iso = data.get("start_time")  # ISO datetime string
    end_iso = data.get("end_time")

    if not court_id or not start_iso or not end_iso:
        return jsonify({"msg": "court_id, start y end son requeridos"}), 400

    try:
        start = datetime.fromisoformat(start_iso)
        end = datetime.fromisoformat(end_iso)
    except Exception:
        return jsonify({"msg": "formato de fecha inválido"}), 400

    if start >= end:
        return jsonify({"msg": "start debe ser anterior a end"}), 400

    # revisar solapamientos
    conflict = Booking.query.filter(
        Booking.court_id == court_id,
        Booking.start_time < end,
        Booking.end_time > start
    ).first()
    if conflict:
        return jsonify({"msg": "franja ya reservada"}), 409

    court = Court.query.get(court_id)
    if not court:
        return jsonify({"msg": "cancha no encontrada"}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "usuario no encontrado"}), 404

    # calcular precio (ejemplo simple proporcional a horas)
    hours = Decimal(str((end - start).total_seconds() / 3600.0))
    base_price = court.price_member if user.is_member else court.price_guest
    total = base_price * hours

    booking = Booking(user_id=user_id, court_id=court_id, start_time=start, end_time=end, price=total)
    db.session.add(booking)
    db.session.commit()

    return jsonify({"msg": "reserva creada", "booking_id": booking.id}), 201

# Eliminar una reserva
@bp.route("/<int:booking_id>", methods=["DELETE"])
@jwt_required()
def cancel_booking(booking_id):
    """Permite al usuario cancelar su propia reserva."""
    user_id = int(get_jwt_identity())

    # 1. Buscar la reserva por ID
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"msg": "Reserva no encontrada"}), 404

    # 2. Verificar que el usuario sea el dueño de la reserva
    if booking.user_id != user_id:
        return jsonify({"msg": "Acceso no autorizado para cancelar esta reserva"}), 403 # Forbidden

    # 3. (Opcional) Implementar lógica de cancelación tardía (ej. no permitir cancelar 1 hora antes)
    # from datetime import datetime, timedelta, timezone
    # if (booking.start_time - datetime.now(timezone.utc)) < timedelta(hours=1):
    #     return jsonify({"msg": "No se puede cancelar una reserva con menos de 1 hora de anticipación"}), 400

    # 4. Eliminar la reserva
    db.session.delete(booking)
    db.session.commit()

    return jsonify({"msg": "Reserva cancelada exitosamente", "booking_id": booking_id}), 200