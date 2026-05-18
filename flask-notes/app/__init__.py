from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

db = SQLAlchemy()           
migrate = Migrate()         
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.notes import notes as notes_blueprint
    app.register_blueprint(notes_blueprint)

    return app