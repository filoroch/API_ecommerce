# ==============================================
# BIBLIOTECAS NECESSÁRIAS (SEM ELAS NADA FUNCIONA)
# ==============================================
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ==============================================
# CONFIGURAÇÃO INICIAL (O "CENÁRIO" DA APLICAÇÃO)
# ==============================================
app = Flask(__name__)
app.config['SECRET_KEY'] = "czfxfrd0"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Altere para True em produção
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

CORS(app, 
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": ["http://localhost:3000"],  # Altere conforme seu frontend
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    }
)

# ==============================================
# MODELOS (COMO OS DADOS SÃO ARMAZENADOS NO BANCO)
# ==============================================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# ==============================================
# FUNÇÕES ESSENCIAIS (MOTORES DA APLICAÇÃO)
# ==============================================
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ==============================================
# ROTAS DE AUTENTICAÇÃO
# ==============================================
@app.route('/register', methods=['POST'])
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

@app.route('/login', methods=['POST'])
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

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout bem-sucedido"})

# ==============================================
# ROTAS DE PRODUTOS
# ==============================================
@app.route('/api/products/add', methods=['POST'])
@login_required
def add_product():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        description = data.get('description', '')

        if not name or price is None:
            return jsonify({'error': 'Nome e preço são obrigatórios'}), 400

        new_product = Product(name=name, price=price, description=description)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Produto adicionado com sucesso'}), 201

    except Exception as e:
        print(f"[ERRO ADD PRODUCT] {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Produto removido com sucesso'}), 200

    except Exception as e:
        print(f"[ERRO DELETE PRODUCT] {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'description': p.description
        } for p in products
    ])

# ==============================================
# INICIALIZAÇÃO
# ==============================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
