from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.services import facade
print(" auth.py charged !")

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class UserLogin(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate a user and return a JWT"""
        data = api.payload
        user = facade.get_user_by_email(data['email'])

        if not user or not check_password_hash(user.password, data['password']):
            return {'error': 'Invalid email or password'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
