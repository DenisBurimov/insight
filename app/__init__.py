# import sqlalchemy as sa
import os
from dotenv import load_dotenv
from flask import Flask, render_template
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from flask_wtf.csrf import CSRFProtect
from google.cloud.sql.connector import Connector

from app.logger import log


login_manager = LoginManager()
csrf = CSRFProtect()
migration = Migrate()
db = SQLAlchemy()
connector = Connector()


def getconn():
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    db_name = os.environ["POSTGRES_DB"]

    return connector.connect(
        instance_connection_name,
        driver="pg8000",
        user=user,
        password=password,
        db=db_name,
    )


def create_app(environment="development"):
    from config import config
    from app.views import (
        main_blueprint,
        auth_blueprint,
        users_blueprint,
    )
    from app.routes import (
        api_payments_blueprint,
    )

    # Instantiate app.
    app = Flask(__name__)
    load_dotenv()

    # Set app config.
    env = os.environ.get("APP_ENV", environment)
    configuration = config(env)
    app.config.from_object(configuration)
    configuration.configure(app)
    log(log.INFO, "Configuration: [%s]", configuration.APP_ENV)

    if configuration.APP_ENV == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing.db"
    elif configuration.DATABASE_CONNECTION == "cloud":
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+pg8000://"
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"creator": getconn}
    elif configuration.DATABASE_CONNECTION == "local":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI"
        )

    log(log.INFO, "SQLALCHEMY_DATABASE_URI: %s", app.config["SQLALCHEMY_DATABASE_URI"])

    db.init_app(app)
    migration.init_app(app, db)

    from app import models as m  # noqa: F401

    # Set up extensions.
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints.
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blueprint)

    # Api routes
    app.register_blueprint(api_payments_blueprint, url_prefix="/api/v1/payments")

    # Set up Flask-Login.
    @login_manager.user_loader
    def get_user(id: int):
        query = sa.select(m.User).where(m.User.id == int(id))
        return db.session.scalar(query)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = m.AnonymousUser

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code

    from app.controllers.jinja_globals import (
        time_without_seconds,
    )

    app.jinja_env.globals["time_without_seconds"] = time_without_seconds

    return app
