import os
from yacut import app, db

# Конфигурация
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DISK_TOKEN = os.getenv('DISK_TOKEN')

app = create_app()
app.config.from_object(Config)

if __name__ == '__main__':
    app.run(debug=True)
