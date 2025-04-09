from flask import Flask
from app.api import api_bp        # Nouveau : API REST via blueprint
import config
from app.views import main_bp     # Frontend blueprint (HTML)
from app.extensions import bcrypt, jwt, db


def create_app(config_class=config.DevelopmentConfig):

    # Création de l'application
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Enregistrer les blueprints
    app.register_blueprint(api_bp)    # API RESTX montée sur /api/v1/
    app.register_blueprint(main_bp)   # Routes HTML

    return app
