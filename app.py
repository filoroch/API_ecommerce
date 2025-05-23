# ==============================================
# BIBLIOTECAS NECESSÁRIAS (SEM ELAS NADA FUNCIONA)
# ==============================================
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flasgger import Swagger
from models import db, User
from views.routes import register_blueprints

# ==============================================
# CONFIGURAÇÃO INICIAL (O "CENÁRIO" DA APLICAÇÃO)
# ==============================================
app = Flask(__name__)
app.config['SECRET_KEY'] = "czfxfrd0"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Altere para True em produção
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}
swagger = Swagger(app, config=swagger_config, template_file='swagger.yaml')

# Inicialize SQLAlchemy com o app
db.init_app(app)

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

# Registrar blueprints
register_blueprints(app)

# Adiciona uma rota de boas-vindas para a raiz
@app.route('/')
def welcome():
    return {
        "message": "Bem-vindo à API E-commerce",
        "swagger_ui": "/swagger/",
        "status": "online"
    }

# ==============================================
# FUNÇÕES ESSENCIAIS (MOTORES DA APLICAÇÃO)
# ==============================================
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

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
