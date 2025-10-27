"""API-модуль для работы с сокращением и восстановлением ссылок."""

from http import HTTPStatus

from flask import Blueprint, jsonify, request

from yacut.models import URLMap
from yacut.constants import ERR_REQUIRED_URL

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/id/', methods=['POST'])
def add_short_link():
    """
    Создаёт короткую ссылку для переданного URL.

    Возвращает JSON-ответ с короткой ссылкой и исходным URL.
    Обрабатывает возможные ошибки:
    – Отсутствие тела запроса.
    – Отсутствие обязательного поля 'url'.
    – Некорректный или занятый custom_id.
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(message='Отсутствует тело запроса'), (
            HTTPStatus.BAD_REQUEST
        )

    url = data.get('url')
    if not url:
        return jsonify(message=ERR_REQUIRED_URL), HTTPStatus.BAD_REQUEST

    try:
        url_map = URLMap.create(url, data.get('custom_id'))
    except ValueError as error:
        return jsonify(message=str(error)), HTTPStatus.BAD_REQUEST

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@api_bp.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    Возвращает исходный URL по короткому идентификатору.

    Если идентификатор не найден, возвращает ошибку 404.
    """
    url_map = URLMap.get_by_short(short_id)
    if not url_map:
        return jsonify(message='Указанный id не найден'), (
            HTTPStatus.NOT_FOUND
        )
    return jsonify(url=url_map.original), HTTPStatus.OK
