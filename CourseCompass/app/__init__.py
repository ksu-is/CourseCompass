from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/grades.db'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'michael.mcgrath.2024@gmail.com'  # your actual Gmail address
app.config['MAIL_PASSWORD'] = 'fito inrw nvpr tadj'  # <- Paste the 16-char app password here


    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.routes import register_routes
    register_routes(app)

    return app
