from flask_restx import Namespace, Resource, fields
from app.services import facade
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Invalid password data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Hash the password before saving
            user_data['password'] = generate_password_hash(user_data['password'])
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'message': 'User successfully created'}, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_safe_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        try:
            # If the password is provided in the update request, hash it before saving
            if 'password' in user_data:
                user_data['password'] = generate_password_hash(user_data['password'])

            updated_user = facade.update_user(user_id, user_data)

            if not updated_user:
                return {'error': 'Update failed'}, 400

            return {'id': updated_user.id, 'message': 'User updated successfully', 'data': updated_user.to_dict()}, 200

        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        try:
            facade.delete_user(user_id)
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
