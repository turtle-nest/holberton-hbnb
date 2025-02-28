from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app.persistence.repository import InMemoryRepository

ns = Namespace("users", description="Operations related to users")

user_model = ns.model("User", {
    "id": fields.String(readonly=True),
    "first_name": fields.String(required=True, description="User's first name"),
    "last_name": fields.String(required=True, description="User's last name"),
    "email": fields.String(required=True, description="User's email address"),
    "password": fields.String(required=True, description="User's password"),
})

repo = InMemoryRepository()
print(repo.get_all())  # Testing

@ns.route("/")
class UserList(Resource):
    @ns.response(200, "List of users retrieved successfully")
    @ns.response(500, "Internal server error")
    def get(self):
        """Return list of users"""
        try:
            users = repo.get_all()
            # Return a dictionary, Flask will automatically convert it to JSON
            return {"users": [{"id": u.id, "first_name": u.first_name, "last_name": u.last_name, "email": u.email} for u in users]}, 200
        except Exception as e:
            return {"error": "An error occurred while retrieving users"}, 500

    @ns.expect(user_model)
    @ns.response(201, "User successfully created")
    @ns.response(400, "Invalid input data")
    @ns.response(500, "Internal server error")
    def post(self):
        """Create a new user"""
        data = request.json
        print(f"Received data: {data}")  # Debug

        # Validation des données
        if not data.get("first_name") or not data.get("last_name") or not data.get("email") or not data.get("password"):
            print("Validation failed: missing fields")  # Debug
            return {"error": "All fields are required"}, 400

        try:
            user = User(**data)
            print(f"Created user object: {user}")  # Debug
            repo.add(user)
            print("User added to repository")  # Debug
            # Return a dictionary with the success message and user ID
            return {"message": "User created", "id": user.id}, 201
        except Exception as e:
            print(f"Error while creating user: {str(e)}")  # Debug
            return {"error": "An error occurred while creating the user"}, 500

@ns.route("/<string:user_id>")
class UserResource(Resource):
    @ns.response(200, "User details retrieved successfully")
    @ns.response(404, "User not found")
    @ns.response(500, "Internal server error")
    def get(self, user_id):
        """Return a user by ID"""
        print(f"Searching for user with ID: {user_id}")  # Testing
        try:
            user = repo.get(user_id)
            if not user:
                print("User not found")  # Testing
                return {"error": "User not found"}, 404
            return {"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email}, 200
        except Exception as e:
            print(f"Error: {str(e)}")  # Testing
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

            return {"message": "User updated", "id": user.id}, 200
        except Exception as e:
            return {"error": "An error occurred while updating the user"}, 500
