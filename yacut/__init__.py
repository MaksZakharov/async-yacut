"""Инициализация Flask-приложения и настройка конфигурации."""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = Path(__file__).parent.parent
dotenv_path = basedir / '.env'
load_dotenv(dotenv_path)

db = SQLAlchemy()


class Config:
    """Конфигурация приложения Flask."""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', 'dev-secret-key-change-in-production'
    )
    DISK_TOKEN = os.getenv('DISK_TOKEN')


def create_app():
    """Создаёт и настраивает экземпляр Flask-приложения."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from . import api_views, views
        from .error_handlers import init_error_handlers

        app.register_blueprint(views.bp)
        app.register_blueprint(api_views.api_bp)

        init_error_handlers(app)
        db.create_all()

    return app


app = create_app()
