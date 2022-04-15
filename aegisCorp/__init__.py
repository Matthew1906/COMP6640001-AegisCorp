from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import getenv, path
from pandas import read_csv

# Create Database
db = SQLAlchemy()

# Load Environment Variables
load_dotenv()

# Configure Locale
setlocale(LC_ALL, 'id_ID.utf8')

def create_app():
    # Create App
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')

    # Config Database URL
    if getenv('DATABASE_URL') == None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aegis-corp.db'
    else: 
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL').replace("postgres", "postgresql")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Database
    db.init_app(app)
    
    # Insert routes
    from .routes.auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from .routes.hospital import hospital
    app.register_blueprint(hospital, url_prefix='/')

    from .routes.insurance import insurance
    app.register_blueprint(insurance, url_prefix='/')

    from .routes.user import user
    app.register_blueprint(user, url_prefix='/')

    # create_database(app)

    from .models import User
    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Default loading user function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app