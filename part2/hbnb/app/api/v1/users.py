from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app.persistence.repository import InMemoryRepository

ns = Namespace("users", description="Operations related to users")

user_model = ns.model("User", {
    "id": fields.String(readonly=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
})

repo = InMemoryRepository()

@ns.route("/")
class UserList(Resource):
    def get(self):
        """Return list of users"""
        users = repo.get_all()
        return jsonify([{"id": u.id, "first_name": u.first_name, "last_name": u.last_name, "email": u.email} for u in users])

    @ns.expect(user_model)
    def post(self):
        """Create a new user"""
        data = request.json
        user = User(**data)
        repo.add(user)
        return jsonify({"message": "User created", "id": user.id})

@ns.route("/<string:user_id>")
class UserResource(Resource):
    def get(self, user_id):
        """Return a user by ID"""
        user = repo.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return jsonify({"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email})

    @ns.expect(user_model)
    def put(self, user_id):
        """Update an user"""
        user = repo.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.json
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.save()

        return jsonify({"message": "User updated", "id": user.id})
