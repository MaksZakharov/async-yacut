"""Константы для сервиса сокращения ссылок YaCut."""

import re

# --- Настройки идентификаторов ---
SHORT_ID_LEN = 6
MAX_ORIGINAL_LENGTH = 500
MAX_SHORT_LENGTH = 16
SHORT_ID_PATTERN = r'[A-Za-z0-9]{1,16}'
ALLOWED_CUSTOM_ID_RE = re.compile(r'^[A-Za-z0-9]+$')

# --- Зарезервированные значения ---
FORBIDDEN_SHORT = 'files'
RESERVED_SHORT_IDS = {'files'}

# --- Тексты ошибок ---
ERR_INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки.'
ERR_REQUIRED_URL = '"url" является обязательным полем!'
ERR_CUSTOM_ID_TAKEN = (
    'Предложенный вариант короткой ссылки уже существует.'
)

# --- Генерация коротких ссылок ---
SHORT_ID_LEN = 6
MAX_ATTEMPTS = 10