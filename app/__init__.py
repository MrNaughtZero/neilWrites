from flask import Flask, Blueprint
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

from .routes import main,admin,auth
 
app.register_blueprint(main.main_bp) 
app.register_blueprint(admin.admin_bp)
app.register_blueprint(auth.auth_bp)

from app.database import setup_db

setup_db(app, os.environ.get('DB_PATH'))

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import Admin

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))