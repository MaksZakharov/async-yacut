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
from yacut.constants import (
    MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH,
    SHORT_ID_PATTERN,
    FORBIDDEN_SHORT,
    ERR_CUSTOM_ID_TAKEN,
)


class URLMapForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректный URL'),
            Length(
                max=MAX_ORIGINAL_LENGTH,
                message='Ссылка превышает допустимую длину',
            ),
        ],
    )

    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                min=1,
                max=MAX_SHORT_LENGTH,
                message='Недопустимая длина короткой ссылки',
            ),
            Optional(),
            Regexp(
                SHORT_ID_PATTERN,
                message='Указано недопустимое имя для короткой ссылки',
            ),
        ],
    )

    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        """Проверяет, что custom_id допустим и не занят."""
        if not field.data:
            return

        if field.data == FORBIDDEN_SHORT:
            raise ValidationError(ERR_CUSTOM_ID_TAKEN)

        if URLMap.get_by_short(field.data):
            raise ValidationError(ERR_CUSTOM_ID_TAKEN)


class FileUploadForm(FlaskForm):
    """Форма для загрузки нескольких файлов."""

    files = MultipleFileField(
        'Выберите файлы',
        validators=[
            DataRequired(message='Необходимо выбрать хотя бы один файл'),
        ],
    )
    submit = SubmitField('Загрузить')
