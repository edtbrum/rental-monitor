from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import IntegrityError
from functools import wraps
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Não autenticado"}), 401
        return f(*args, **kwargs)
    return decorated_function
# ---------------------------------------------------------------
@auth_bp.route("/login", methods=['POST'])
def login_route():
    data = request.get_json()

    try:
        service = UserService()
        response = service.login_user(data)
        if not response or "error" in response:
            return jsonify({"error": "Credenciais inválidas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    session['user_id'] = response['id']
    session['username'] = response['username']
    session['email'] = response['email']

    return jsonify(response), 200
# ---------------------------------------------------------------
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({"message": "Logout realizado com sucesso"}), 200
# ---------------------------------------------------------------
@auth_bp.route("/user", methods=['POST'])
def create_user_route():
    data = request.get_json()

    try:
        service = UserService()
        response = service.create_user(data)
    except IntegrityError:
        return jsonify({"error": "Conflito: Username ou Email já existe"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(response), 200
# ---------------------------------------------------------------
@auth_bp.route("/user", methods=['PUT'])
@login_required
def update_user_route():
    username = request.args.get('username')
    data = request.get_json()

    if not username:
        return jsonify({"error": "O parâmetro 'username' é obrigatório"}), 400
    
    try:
        service = UserService()
        response = service.update_user(username, data)
        if not response:
            return jsonify({"error": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(response), 200
# ---------------------------------------------------------------
@auth_bp.route("/user", methods=['DELETE'])
def delete_user_route():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "O parâmetro 'username' é obrigatório"}), 400

    try:
        service = UserService()
        response = service.delete_user(username)
        if not response:
            return jsonify({"error": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify(response), 200
# ---------------------------------------------------------------