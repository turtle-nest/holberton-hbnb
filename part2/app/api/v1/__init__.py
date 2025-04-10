from flask import Blueprint
from flask_restx import Api

bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api = Api(bp, version="1.0", title="HBnB API", description="API for HBnB")

from app.api.v1.users import ns as user_ns
api.add_namespace(user_ns)
