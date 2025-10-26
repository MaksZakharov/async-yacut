"""Обработчики ошибок для пользовательского интерфейса и API."""

from http import HTTPStatus

from flask import jsonify, render_template, request

from yacut import db


def init_error_handlers(app):
    """Инициализирует обработчики ошибок для приложения Flask."""

    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request_error(error):
        """Обрабатывает ошибку 400 — неверный запрос."""
        if request.path.startswith('/api/'):
            return jsonify({'message': 'Неверный запрос'}), (
                HTTPStatus.BAD_REQUEST
            )
        return render_template(
            '400.html',
            error_code=HTTPStatus.BAD_REQUEST,
            error_message='Неверный запрос'
        ), HTTPStatus.BAD_REQUEST

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found_error(error):
        """Обрабатывает ошибку 404 — страница не найдена."""
        if request.path.startswith('/api/'):
            return jsonify({'message': 'Указанный id не найден'}), (
                HTTPStatus.NOT_FOUND
            )
        return render_template(
            'error.html',
            error_code=HTTPStatus.NOT_FOUND,
            error_message='Страница не найдена'
        ), HTTPStatus.NOT_FOUND

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def internal_error(error):
        """Обрабатывает ошибку 500 — внутренняя ошибка сервера."""
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify(
                {'message': 'Внутренняя ошибка сервера'}
            ), HTTPStatus.INTERNAL_SERVER_ERROR
        return render_template(
            '500.html',
            error_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_message='Внутренняя ошибка сервера'
        ), HTTPStatus.INTERNAL_SERVER_ERROR
