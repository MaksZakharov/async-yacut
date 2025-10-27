# Yacut

Yacut — это сервис для сокращения ссылок. 
Он позволяет создавать короткие ссылки для удобного обмена и отслеживания переходов.

## 🚀 Функционал

- Сокращение длинных ссылок.
- Возможность указать собственный короткий идентификатор.
- Автоматическая генерация уникальных коротких ссылок.
- Переадресация по короткому адресу на оригинальный.
- API для работы с сервисом.
- Загрузка файлов на сервер через отдельную страницу.

## 🛠️ Технологии

- **Python 3.9+**
- **Flask**
- **SQLAlchemy**
- **WTForms**
- **Flask-Migrate**
- **Jinja2**
- **SQLite** (на этапе разработки)

## ⚙️ Установка и запуск

Клонируйте репозиторий и перейдите в него в командной строке:

```bash
git clone <ссылка-на-репозиторий>
cd yacut
```

Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
# Для Linux/macOS
source venv/bin/activate
# Для Windows
source venv/Scripts/activate
```

Установите зависимости:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Создайте файл `.env` в корневой директории проекта и укажите переменные окружения:

```
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_token
```

Создайте базу данных и примените миграции:

```bash
flask db upgrade
```

Запустите приложение:

```bash
flask run
```

После запуска проект будет доступен по адресу:  
👉 http://127.0.0.1:5000/

## 📁 Структура проекта

```
yacut/
├── __init__.py
├── api_views.py
├── forms.py
├── models.py
├── views.py
├── static/
└── templates/
```

## 👤 Автор

**Макс Захаров**  
Python Developer | [GitHub: MaksZakharov](https://github.com/MaksZakharov)
