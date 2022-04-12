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

    from .models import User

    # create_database(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Default loading user function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app