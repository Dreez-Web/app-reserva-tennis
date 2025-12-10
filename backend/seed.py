from app import create_app, db
from app.models import User, Court
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Crear admin
    admin = User(
        email="admin@local",
        password_hash=generate_password_hash("admin123"),
        role="admin",
        is_member=True
    )
    db.session.add(admin)

    # Crear canchas
    c1 = Court(name="Cancha 1", sport="tennis", price_member=8.00, price_guest=16.00)
    c2 = Court(name="Cancha 2", sport="tennis", price_member=9.00, price_guest=18.00)
    db.session.add_all([c1, c2])

    db.session.commit()
    print("Datos iniciales creados!")
