"""API-модуль для работы с сокращением и восстановлением ссылок."""

import re
from http import HTTPStatus

from flask import Blueprint, jsonify, request

from yacut import db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/id/', methods=['POST'])
def add_short_link():
    """
    Создаёт короткую ссылку для переданного URL.

    Возвращает JSON-ответ с короткой ссылкой и исходным URL.
    Обрабатывает возможные ошибки:
    - Отсутствие тела запроса.
    - Отсутствие обязательного поля 'url'.
    - Некорректный или уже существующий custom_id.
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(message='Отсутствует тело запроса'), (
            HTTPStatus.BAD_REQUEST
        )

    if 'url' not in data:
        return jsonify(
            message='"url" является обязательным полем!'
        ), HTTPStatus.BAD_REQUEST

    custom_id = data.get('custom_id')
    if custom_id:
        # Только латиница и цифры, длина 1–16, и не зарезервированное 'files'
        if custom_id == 'files' or not re.fullmatch(r'[A-Za-z0-9]{1,16}', 
                                                    custom_id):
            return jsonify(
                message='Указано недопустимое имя для короткой ссылки'
            ), HTTPStatus.BAD_REQUEST

        if URLMap.query.filter_by(short=custom_id).first():
            return jsonify(
                message=('Предложенный вариант короткой ссылки '
                         'уже существует.')
            ), HTTPStatus.BAD_REQUEST
        short_id = custom_id
    else:
        short_id = get_unique_short_id()

    url_map = URLMap(original=data['url'], short=short_id)
    db.session.add(url_map)
    db.session.commit()

    return jsonify(
        short_link=f"{request.host_url.rstrip('/')}/{short_id}",
        url=url_map.original,
    ), HTTPStatus.CREATED


@api_bp.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    Возвращает исходный URL по переданному короткому идентификатору.

    Если идентификатор не найден, возвращает ошибку 404.
    """
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify(
            message='Указанный id не найден'
        ), HTTPStatus.NOT_FOUND
    return jsonify(url=url_map.original), HTTPStatus.OK
