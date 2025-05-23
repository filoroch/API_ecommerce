# routes.py
# Definição das rotas Flask

from flask import Blueprint
from controllers.auth_controller import auth_bp
from controllers.product_controller import product_bp

views_bp = Blueprint('views', __name__)

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
