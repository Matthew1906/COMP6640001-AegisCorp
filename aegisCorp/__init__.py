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
    from .routes.views import views
    app.register_blueprint(views, url_prefix='/')

    from .routes.auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from .routes.hospital import hospital
    app.register_blueprint(hospital, url_prefix='/')

    from .routes.insurance import insurance
    app.register_blueprint(insurance, url_prefix='/')

    from .routes.customer import customer
    app.register_blueprint(customer, url_prefix='/')

    # Initialize Database (if necessary)
    # create_database(app)
 
    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Default loading user function
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    return app

def create_database(app):
    db.create_all(app=app)
    with app.app_context():
        table_names = [
            'doctors', 'hospital_staffs', 
            'hospitals','policies', 
            'insurance_staffs', 'companies',
            'medications', 'procedure_types',
            'procedures','users'
        ]
        for table_name in table_names:
            df = read_csv(f'./resources/{table_name}.csv', delimiter=',', index_col=0)             
            name = table_name.split("_")[0] + table_name.split("_")[1].capitalize()\
                if table_name.find("_")!=-1 else table_name
            df.to_sql(name = name, con = db.engine, if_exists = 'append', index = False)