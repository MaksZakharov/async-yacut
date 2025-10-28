"""Модель базы данных для хранения коротких и оригинальных ссылок."""

import random
import re
import string
from datetime import datetime

from flask import url_for

from yacut import db
from yacut.constants import (
    FORBIDDEN_SHORT,
    MAX_ATTEMPTS,
    MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH,
    SHORT_ID_LEN,
    SHORT_ID_PATTERN,
)
from yacut.exceptions import ShortIDGenerationError


class URLMap(db.Model):
    """Модель URLMap: хранит оригинальную и сокращённую ссылку."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(MAX_ORIGINAL_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(MAX_SHORT_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Возвращает словарь с данными ссылки."""
        return {
            'url': self.original,
            'short_link': url_for(
                'main.redirect_to_original',
                short_id=self.short,
                _external=True
            ),
        }

    @staticmethod
    def get_by_short(short_id):
        """Возвращает объект URLMap по короткому идентификатору."""
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def create(original, custom_id=None):
        """
        Создаёт новую запись URLMap.

        Выполняет валидацию пользовательского идентификатора,
        генерирует уникальный при отсутствии кастомного.
        """
        if custom_id:
            if (custom_id == FORBIDDEN_SHORT
                    or not re.fullmatch(SHORT_ID_PATTERN, custom_id)):
                raise ValueError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if URLMap.get_by_short(custom_id):
                raise ValueError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            short = custom_id
        else:
            short = URLMap.generate_short_id()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def generate_short_id():
        """Создаёт уникальный короткий идентификатор."""
        characters = string.ascii_letters + string.digits
        for _ in range(MAX_ATTEMPTS):
            short_id = ''.join(random.choices(characters, k=SHORT_ID_LEN))
            if (short_id != FORBIDDEN_SHORT
                    and not URLMap.get_by_short(short_id)):
                return short_id
        raise ShortIDGenerationError(
            'Не удалось сгенерировать уникальный короткий ID'
        )
    