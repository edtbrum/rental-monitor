from flask import Flask
from config import Config
from .extensions import db, migrate
from .routes.auth_routes import auth_bp
import app.models

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)

    return app