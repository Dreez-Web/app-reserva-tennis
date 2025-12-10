from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    # 🚨 COLUMNA AÑADIDA
    name = db.Column(db.String(100), nullable=True) 
    
    password_hash = db.Column(db.String(255), nullable=True) 
    is_member = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default="user") 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", back_populates="user")

class Court(db.Model):
    __tablename__ = "courts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    sport = db.Column(db.String(50), default="tennis")
    # precio base por hora (puedes ajustar)
    price_member = db.Column(db.Numeric(8,2), default=10.00)
    price_guest = db.Column(db.Numeric(8,2), default=20.00)

    bookings = db.relationship("Booking", back_populates="court")

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey("courts.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(8,2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="bookings")
    court = db.relationship("Court", back_populates="bookings")