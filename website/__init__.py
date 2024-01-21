import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()  # Create 'mail' object at the module level

def create_app():
    app = Flask(__name__)
    from dotenv import load_dotenv

    load_dotenv()
    app.config['SECRET_KEY'] =  os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    migrate = Migrate(app, db)
    db.init_app(app)
    
    # Email configuration
    app.config['MAIL_SERVER'] =  os.environ.get("MAIL_SERVER")
    app.config['MAIL_PORT'] =  os.environ.get("MAIL_PORT")
    app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS")
    app.config['MAIL_USERNAME'] =  os.environ.get("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] =  os.environ.get("MAIL_PASSWORD")

    mail.init_app(app)  # Initialize the 'mail' object here
    
    from .views import views
    from .auth import auth
    from .shows import shows
    from .emails import emails
    from .superstars import superstars
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(shows, url_prefix="/")
    app.register_blueprint(emails, url_prefix="/")
    app.register_blueprint(superstars, url_prefix="/")
    
    from .models import User
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

from .models import User
from werkzeug.security import generate_password_hash

def create_database(app):
    with app.app_context():
        db.create_all()
        print("Created Database!")
        
        # Create admin user
        admin_email = "emililiev2001@abv.bg"
        admin_username = "admin"
        admin_password = "aaa"
        
        
        
        admin = User.query.filter(User.email == admin_email).first()
        if not admin:
            admin = User(email=admin_email, username=admin_username, password=generate_password_hash(admin_password), role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
        else:
            print("Admin user already exists.")