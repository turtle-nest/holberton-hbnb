from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
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
        print("📩 Requête reçue dans POST /login")
        credentials = api.payload  # Get the email and password from the request payload
        print("🔑 Credentials reçus:", credentials)

        try:
            user = facade.get_user_by_email(credentials['email'])
            print("👤 Utilisateur trouvé:", user)
        except Exception as e:
            print("❌ Erreur dans get_user_by_email:", e)
            return {'error': 'Erreur lors de la récupération de l’utilisateur'}, 500

        if not user or not user.verify_password(credentials['password']):
            print("❌ Mauvais identifiants")
            return {'error': 'Invalid credentials'}, 401

        try:
            access_token = create_access_token(
                identity=user.id,
                additional_claims={'is_admin': user.is_admin}
            )
            print("✅ Token généré")
        except Exception as e:
            print("❌ Erreur JWT:", e)
            return {'error': str(e).strip("'")}, 500

        return {'access_token': access_token}, 200
