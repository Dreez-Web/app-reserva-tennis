from flask import Blueprint, request, jsonify
from ..models import Court, Booking
from .. import db
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required # Importante para proteger la ruta

bp = Blueprint("courts", __name__)

@bp.route("/", methods=["GET"])
@jwt_required() # ⬅️ Protege la ruta: requiere un token JWT válido
def list_courts():
    """Devuelve la lista de canchas disponibles, solo para usuarios logueados."""
    
    # 1. Consulta a la base de datos
    courts = Court.query.all()
    
    # 2. Formateo de los resultados
    result = [{
        "id": c.id, 
        "name": c.name, 
        "sport": c.sport,
        # Convertir Decimal o float a string para evitar problemas de serialización JSON
        "price_member": str(c.price_member), 
        "price_guest": str(c.price_guest)    
    } for c in courts]
    
    return jsonify(result), 200

@bp.route("/<int:court_id>/availability", methods=["GET"])
def availability(court_id):
    """Devuelve las franjas horarias disponibles para una cancha específica en una fecha dada."""
    
    # Query param date=YYYY-MM-DD
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"msg": "date required YYYY-MM-DD"}), 400
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"msg": "formato de fecha inválido"}), 400

    # ejemplo: franjas de 1h desde 08:00 a 22:00
    start_hour = 8
    end_hour = 22
    slots = []
    
    for h in range(start_hour, end_hour):
        start = datetime.combine(date, datetime.min.time()) + timedelta(hours=h)
        end = start + timedelta(hours=1)
        
        # Comprobar si existe un booking que se solape en esa franja horaria
        conflict = Booking.query.filter(
            Booking.court_id == court_id,
            Booking.start_time < end,
            Booking.end_time > start
        ).first()
        
        slots.append({
            "start": start.isoformat(),
            "end": end.isoformat(),
            "available": conflict is None
        })
        
    return jsonify(slots), 200