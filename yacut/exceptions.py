"""Пользовательские исключения для проекта YaCut."""


class ShortIDGenerationError(Exception):
    """Ошибка генерации уникального короткого идентификатора."""
    pass


class YandexAPIError(Exception):
    """Базовая ошибка при обращении к API Яндекс.Диска."""
    pass


class YandexUploadError(YandexAPIError):
    """Ошибка при загрузке файла на Яндекс.Диск."""
    pass


class YandexDownloadError(YandexAPIError):
    """Ошибка при получении ссылки на скачивание с Яндекс.Диска."""
    pass
