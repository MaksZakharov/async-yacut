"""Основные view-функции: главная страница, загрузка файлов и редиректы."""

import asyncio
from http import HTTPStatus
from io import BytesIO

import requests
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from yacut import db
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import (
    get_unique_short_id,
    yandex_get_download_link,
    yandex_upload_file,
)

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    """Главная страница для создания коротких ссылок."""
    form = URLMapForm()
    short_link = None

    if form.validate_on_submit():
        short_id = form.custom_id.data or get_unique_short_id()

        if short_id == 'files':
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        if URLMap.query.filter_by(short=short_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        url_map = URLMap(original=form.original_link.data, short=short_id)
        db.session.add(url_map)
        db.session.commit()

        short_link = request.host_url.rstrip('/') + '/' + short_id

    return render_template('index.html', form=form, short_link=short_link)


@bp.route('/files', methods=['GET', 'POST'])
def files():
    """Страница загрузки файлов на Яндекс.Диск."""
    form = FileUploadForm()
    uploaded_files = []

    if request.method == 'POST' and form.validate_on_submit():
        files_data = request.files.getlist('files')
        if files_data and any(f.filename for f in files_data):
            disk_token = (
                current_app.config.get('YANDEX_DISK_OAUTH_TOKEN')
                or current_app.config.get('YANDEX_DISK_TOKEN')
                or current_app.config.get('DISK_TOKEN')
                or 'test-token'
            )
            try:
                uploaded_files = asyncio.run(
                    upload_files_to_disk(
                        files_data,
                        disk_token,
                        request.host_url
                    )
                )
                if not uploaded_files:
                    flash('Не удалось загрузить файлы на Яндекс.Диск.')
            except Exception as e:
                current_app.logger.error('Error uploading files: %s', e)
                flash(f'Ошибка при загрузке файлов: {e}')

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files
    )


async def upload_files_to_disk(files_data, disk_token, host_url):
    """Асинхронная загрузка файлов на Яндекс.Диск."""
    uploaded_files = []
    url_maps = []

    for file in files_data:
        if not file.filename:
            continue
        try:
            file_path = await yandex_upload_file(
                file, 
                file.filename, 
                disk_token
            )
            try:
                _ = await yandex_get_download_link(file_path, disk_token)
            except Exception:
                current_app.logger.exception('Prefetch download link failed')

            short_id = get_unique_short_id()
            url_maps.append(URLMap(original=file_path, short=short_id))
            short_link = host_url.rstrip('/') + '/' + short_id
            uploaded_files.append(
                {'filename': file.filename, 'short_link': short_link}
            )
        except Exception as e:
            current_app.logger.error(
                'Error uploading %s: %s',
                file.filename,
                e
            )

    if url_maps:
        db.session.add_all(url_maps)
        db.session.commit()

    return uploaded_files


@bp.route('/<short_id>')
def redirect_to_original(short_id):
    """Переадресует по короткой ссылке или выдаёт файл с Яндекс.Диска."""
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    original = url_map.original

    is_disk_path = original.startswith('/') or original.startswith('app:/')
    if not is_disk_path:
        return redirect(original, code=HTTPStatus.FOUND)

    disk_token = (
        current_app.config.get('YANDEX_DISK_OAUTH_TOKEN')
        or current_app.config.get('YANDEX_DISK_TOKEN')
        or current_app.config.get('DISK_TOKEN')
    )
    if not disk_token:
        current_app.logger.error('No Yandex.Disk token configured')
        flash('Отсутствует токен Яндекс.Диска')
        return redirect(url_for('main.files'))

    try:
        download_meta = requests.get(
            'https://cloud-api.yandex.net/v1/disk/resources/download',
            headers={'Authorization': f'OAuth {disk_token}'},
            params={'path': original},
            timeout=20,
        )
        download_meta.raise_for_status()
        href = download_meta.json().get('href')
        if not href:
            raise RuntimeError('В ответе нет href')
    except Exception as e:
        current_app.logger.exception('Yandex href error: %s', e)
        flash('Не удалось получить ссылку на скачивание файла.')
        return redirect(url_for('main.files'))

    try:
        file_resp = requests.get(href, timeout=120)
        file_resp.raise_for_status()

        name_part = original.replace('app:', '').lstrip(':/')
        filename = name_part.rsplit('/', 1)[-1] or 'file'

        mime = file_resp.headers.get(
            'Content-Type',
            'application/octet-stream'
        )
        buf = BytesIO(file_resp.content)
        buf.seek(0)

        return send_file(
            buf,
            mimetype=mime,
            as_attachment=True,
            download_name=filename,
            max_age=0,
            conditional=False,
        )
    except Exception as e:
        current_app.logger.exception('File proxy error: %s', e)
        flash('Не удалось скачать файл с Яндекс.Диска.')
        return redirect(url_for('main.files'))
