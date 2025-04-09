from flask import Blueprint
from flask_restx import Api

# Création du blueprint RESTX
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Création de l'objet API RESTX sur ce blueprint
api = Api(
    api_bp,
    version='1.0',
    title='HBnB API',
    description='HBnB Application API',
    doc='/docs',  # Swagger dispo à /api/v1/docs
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Bearer <JWT>"
        }
    }
)

# Import et ajout des namespaces (fais ici ou dans __init__.py racine si tu préfères)
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns

api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(protected_ns, path='/protected')
