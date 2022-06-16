import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from manager_demo.config import get_config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_file(get_config(), load=json.load)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from manager_demo.users.routes import users
    from manager_demo.roles.routes import roles
    from manager_demo.projects.routes import projects
    from manager_demo.main.routes import main
    from manager_demo.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(roles)
    app.register_blueprint(projects)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
