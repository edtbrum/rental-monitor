from app.schemas.user_schema import UserCreateSchema, UserResponseSchema, UserBaseSchema
from app.schemas.user_schema import UserLoginSchema
from app.repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db

class UserService:

    def login_user(self, data):
        schema = UserLoginSchema()
        response = UserResponseSchema()
        repo = UserRepository(db.session)

        validated_data = schema.load(data)
        user = repo.get_by_username(validated_data['username'])
        if user is None:
            return None
        
        if not check_password_hash(user.password_hash, validated_data['password']):
            return {"error": "Senha inválida"}

        return response.dump(user)
    # ---------------------------------------------------------------
    def create_user(self, data):
        schema = UserCreateSchema()
        response = UserResponseSchema()
        repo = UserRepository(db.session)

        validated_data = schema.load(data)
        password_hash = generate_password_hash(validated_data["password"])
        user_data = {
            "username": validated_data["username"],
            "email": validated_data["email"],
            "password_hash": password_hash
        }

        try:
            user = repo.create(user_data)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

        return response.dump(user)
    # ---------------------------------------------------------------
    def update_user(self, username, data):
        schema = UserBaseSchema()
        response = UserResponseSchema()
        repo = UserRepository(db.session)

        validated_data = schema.load(data)

        try:
            user = repo.update(username, validated_data)
            if user is None:
                return None
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

        return response.dump(user)
    # ---------------------------------------------------------------
    def delete_user(self, username):
        response = UserResponseSchema()
        repo = UserRepository(db.session)

        user = repo.get_by_username(username)
        if user is None:
            return None

        try:
            repo.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

        return response.dump(user)
    # ---------------------------------------------------------------