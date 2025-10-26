"""Формы для создания коротких ссылок и загрузки файлов."""

from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    URL,
    ValidationError,
)

from yacut.models import URLMap


class URLMapForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректный URL'),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                max=16,
                message='Указано недопустимое имя для короткой ссылки',
            ),
            Optional(),
            Regexp(
                r'^[a-zA-Z0-9]*$',
                message='Указано недопустимое имя для короткой ссылки',
            ),
        ],
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        """Проверяет, что custom_id допустим и не занят."""
        if field.data:
            if field.data == 'files':
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            if URLMap.query.filter_by(short=field.data).first():
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )


class FileUploadForm(FlaskForm):
    """Форма для загрузки нескольких файлов."""

    files = MultipleFileField(
        'Выберите файлы',
        validators=[DataRequired(message='Необходимо выбрать файлы')],
    )
    submit = SubmitField('Загрузить')
