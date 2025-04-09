from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations', path='/api/v1/auth')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        try:
            user = facade.get_user_by_email(credentials['email'])
        except Exception as e:
            return {'error': 'Error retrieving user'}, 500

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        try:
            access_token = create_access_token(
                identity={
                    'id': user.id,
                    'first_name': user.first_name,
                    'email': user.email
                },
                additional_claims={'is_admin': user.is_admin}
            )

        except Exception as e:
            return {'error': str(e).strip("'")}, 500

        return {'access_token': access_token}, 200
