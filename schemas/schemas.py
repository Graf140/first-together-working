from marshmallow import Schema, fields, ValidationError, validate, validates_schema

# schemas/user_schema.py
from marshmallow import Schema, fields, ValidationError, validates

class CreateUserSchema(Schema):
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    first_name = fields.Str(required=True)
    middle_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    user_id = fields.Int(required=True)

    @validates('phone')
    def validate_phone(self, value):
        # Простая проверка: хотя бы 7 цифр
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) < 7:
            raise ValidationError("Phone must contain at least 7 digits.")