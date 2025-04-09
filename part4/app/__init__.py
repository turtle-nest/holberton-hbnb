from flask import Flask
from flask_cors import CORS
from app.api import api_bp
from app.views import main_bp
from app.extensions import bcrypt, jwt, db
import config


def create_app(config_class=config.DevelopmentConfig):

    # Création de l'application
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)

    # Enregistrer les blueprints
    app.register_blueprint(api_bp)    # API RESTX montée sur /api/v1/
    app.register_blueprint(main_bp)   # Routes HTML

    return app
