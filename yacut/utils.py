"""Утилиты для генерации коротких ссылок и работы с API Яндекс.Диска."""

import random
import string

import aiohttp

from yacut.models import URLMap

YANDEX_HOST = 'https://cloud-api.yandex.net'
API_VER = 'v1'
UPLOAD_URL = f'{YANDEX_HOST}/{API_VER}/disk/resources/upload'
DOWNLOAD_URL = f'{YANDEX_HOST}/{API_VER}/disk/resources/download'


def get_unique_short_id(length=6):
    """Генерирует уникальный короткий идентификатор переменной длины."""
    characters = string.ascii_letters + string.digits
    max_attempts = 10
    for _ in range(max_attempts):
        short_id = ''.join(random.choices(characters, k=length))
        exists = URLMap.query.filter_by(short=short_id).first()
        if short_id != 'files' and not exists:
            return short_id
    return get_unique_short_id(length + 1)


async def yandex_upload_file(file, filename, disk_token):
    """Загружает файл на Яндекс.Диск, возвращает путь `app:/<filename>`."""
    headers = {'Authorization': f'OAuth {disk_token}'}
    path = f'app:/{filename}'

    async with aiohttp.ClientSession() as session:
        async with session.get(
            UPLOAD_URL,
            headers=headers,
            params={'path': path, 'overwrite': 'true'},
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(
                    f'Не удалось получить upload url: {resp.status} {text}'
                )
            data = await resp.json()
            upload_href = data.get('href')
            if not upload_href:
                raise Exception('Нет href в ответе для upload')

    file.seek(0)
    file_content = file.read()

    async with aiohttp.ClientSession() as session:
        async with session.put(
            upload_href,
            data=file_content,
            timeout=aiohttp.ClientTimeout(total=60),
        ) as resp:
            if resp.status not in (200, 201, 202):
                text = await resp.text()
                raise Exception(
                    f'Не удалось загрузить файл: {resp.status} {text}'
                )

    return path


async def yandex_get_download_link(file_path, disk_token):
    """Возвращает актуальную download-ссылку для пути `app:/<filename>`."""
    headers = {'Authorization': f'OAuth {disk_token}'}
    async with aiohttp.ClientSession() as session:
        async with session.get(
            DOWNLOAD_URL,
            headers=headers,
            params={'path': file_path},
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(
                    f'Не удалось получить download url: {resp.status} {text}'
                )
            data = await resp.json()
            href = data.get('href')
            if not href:
                raise Exception('Нет href в ответе для download')
            return href
