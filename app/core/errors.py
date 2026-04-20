# app/core/errors.py

class AppError(Exception):
    """Типичная  ошибка приложения"""
    pass


class ConflictError(AppError):
    """Конфликт из за повторения данных"""
    pass


class UnauthorizedError(AppError):
    """Неавторизованный пользователь"""
    pass


class ForbiddenError(AppError):
    """Запрет при отсутствии прав"""
    pass


class NotFoundError(AppError):
    """Не найден в БД"""
    pass


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса"""
    pass
