from flask import Blueprint, request, jsonify
from app.services.facade import UserService

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@users_bp.route('/', methods=['GET'])
def get_all_users():
	"""Retourne la liste de tous les utilisateurs (sans mot de passe)."""
	users = UserService.get_all_users()
	return jsonify(users), 200

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
	"""Met à jour un utilisateur existant."""
	data = request.json
	updated_user = UserService.update_user(user_id, data)
	if updated_user:
		return jsonify(updated_user), 200
	return jsonify({"error": "User not found"}), 404
