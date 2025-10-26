"""Константы для сервиса сокращения ссылок."""

import re

ALLOWED_CUSTOM_ID_RE = re.compile(r'^[A-Za-z0-9]+$')
SHORT_ID_LEN = 6
RESERVED_SHORT_IDS = {'files'}

ERR_INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
ERR_REQUIRED_URL = '"url" является обязательным полем!'
ERR_CUSTOM_ID_TAKEN = (
    'Предложенный вариант короткой ссылки уже существует.'
)
