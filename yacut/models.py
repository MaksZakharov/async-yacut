"""Модель базы данных для хранения коротких и оригинальных ссылок."""

from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """Модель URLMap: хранит оригинальную и сокращённую ссылку."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(500), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Возвращает словарь с данными ссылки."""
        return {
            'url': self.original,
            'short_link': self.short,
        }

    def from_dict(self, data):
        """Обновляет поля экземпляра на основе данных словаря."""
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
