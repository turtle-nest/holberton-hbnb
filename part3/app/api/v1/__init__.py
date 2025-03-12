from flask import Blueprint
from flask_restx import Api

from .users import api as users_ns
from .auth import api as auth_ns

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(api_v1)

api.add_namespace(users_ns, path='/users')
api.add_namespace(auth_ns, path='/auth')
