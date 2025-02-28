from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app.persistence.repository import InMemoryRepository

ns = Namespace("users", description="Operations related to users")

user_model = ns.model("User", {
    "id": fields.String(readonly=True),
    "first_name": fields.String(required=True, description="User's first name"),
    "last_name": fields.String(required=True, description="User's last name"),
    "email": fields.String(required=True, description="User's email address"),
})

repo = InMemoryRepository()

@ns.route("/")
class UserList(Resource):
    @ns.response(200, "List of users retrieved successfully")
    @ns.response(500, "Internal server error")
    def get(self):
        """Return list of users"""
        try:
            users = repo.get_all()
            return jsonify([{"id": u.id, "first_name": u.first_name, "last_name": u.last_name, "email": u.email} for u in users])
        except Exception as e:
            return {"error": "An error occurred while retrieving users"}, 500

    @ns.expect(user_model)
    @ns.response(201, "User successfully created")
    @ns.response(400, "Invalid input data")
    @ns.response(500, "Internal server error")
    def post(self):
        """Create a new user"""
        data = request.json
        if not data.get("first_name") or not data.get("last_name") or not data.get("email"):
            return {"error": "All fields are required"}, 400

        try:
            user = User(**data)
            repo.add(user)
            return jsonify({"message": "User created", "id": user.id}), 201
        except Exception as e:
            return {"error": "An error occurred while creating the user"}, 500

@ns.route("/<string:user_id>")
class UserResource(Resource):
    @ns.response(200, "User details retrieved successfully")
    @ns.response(404, "User not found")
    @ns.response(500, "Internal server error")
    def get(self, user_id):
        """Return a user by ID"""
        try:
            user = repo.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
            return jsonify({"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email})
        except Exception as e:
            return {"error": "An error occurred while retrieving the user"}, 500

    @ns.expect(user_model)
    @ns.response(200, "User updated successfully")
    @ns.response(400, "Invalid input data")
    @ns.response(404, "User not found")
    @ns.response(500, "Internal server error")
    def put(self, user_id):
        """Update a user"""
        try:
            user = repo.get(user_id)
            if not user:
                return {"error": "User not found"}, 404

            data = request.json
            if not data:
                return {"error": "Invalid input data"}, 400

            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.email = data.get("email", user.email)
            user.save()

            return jsonify({"message": "User updated", "id": user.id}), 200
        except Exception as e:
            return {"error": "An error occurred while updating the user"}, 500
