from marshmallow import Schema, fields

class UserBaseSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)

class UserCreateSchema(UserBaseSchema):
    password = fields.Str(required=True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserResponseSchema(UserBaseSchema):
    id = fields.Int()
    created_at = fields.DateTime()