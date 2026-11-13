"""Excepciones de negocio. Flask las convierte en JSON."""


class AppException(Exception):
    status_code = 400

    def __init__(self, detail: str = "Error", status_code: int | None = None):
        super().__init__(detail)
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class NotFoundError(AppException):
    status_code = 404


class UnauthorizedError(AppException):
    status_code = 401


class ConflictError(AppException):
    status_code = 409


class ValidationError(AppException):
    status_code = 422