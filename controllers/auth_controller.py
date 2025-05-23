# auth_controller.py
# Lógica de controle para autenticação

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Usuário já existe'}), 409
        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Usuário registrado com sucesso'}), 201
    except Exception as e:
        print(f"[ERRO REGISTRO] {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Dados incompletos"}), 400
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"error": "Credenciais inválidas"}), 401
        login_user(user)
        return jsonify({
            "message": "Login bem-sucedido",
            "user_id": user.id
        }), 200
    except Exception as e:
        print(f"[ERRO LOGIN] {e}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout bem-sucedido"})
