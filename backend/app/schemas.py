from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    is_member = fields.Boolean()
    role = fields.Str()

class CourtSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    sport = fields.Str()
    price_member = fields.Decimal(as_string=True)
    price_guest = fields.Decimal(as_string=True)

class BookingSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    court_id = fields.Int()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    price = fields.Decimal(as_string=True)
