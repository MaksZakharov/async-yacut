"""Модуль конфигурации Flask-приложения."""

import os


class Config:
    """Хранит настройки приложения Flask и параметры окружения."""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
