
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forex.db'

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import auth, robot, subscription
    app.register_blueprint(auth.bp)
    app.register_blueprint(robot.bp)
    app.register_blueprint(subscription.bp)

    return app