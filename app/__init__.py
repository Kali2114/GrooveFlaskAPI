"""Main file app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.commands import db_manage_bp
    from app.errors import errors_bp
    from app.artists import artists_bp
    from app.albums import albums_bp
    from app.auth import auth_bp

    app.register_blueprint(db_manage_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(artists_bp, url_prefix="/api")
    app.register_blueprint(albums_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
