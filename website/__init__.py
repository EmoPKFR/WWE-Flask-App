from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "MySpEci@l5eCr#7Ke!"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    migrate = Migrate(app, db)
    db.init_app(app)
         
    from .views import views
    from .auth import auth
    from .shows import shows
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(shows, url_prefix="/")
    
    from .models import User, Order
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print("Created Database!")
       