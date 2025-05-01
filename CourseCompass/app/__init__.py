from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
mail = Mail()

def create_app():
    import os
    app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance'))


    # Core Config
    app.config['SECRET_KEY'] = 'your-secret-key'
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance', 'grades.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath(db_path)}"


    # Email Config (from .env)
    app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 8025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = 'coursecompass@outlook.com'

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

    # Register routes
    from app.routes import register_routes
    register_routes(app)

    return app
