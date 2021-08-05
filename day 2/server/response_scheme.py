from enum import Enum
from flask import jsonify
from time import time


class Errors(Enum):
    DEFAULT_PARSE_ERROR = (1, 400, "default_parse_error", "Произошла ошибка")
    METHOD_NOT_ALLOWED = (2, 405, "method_not_allowed", "Этот метод запроса не поддерживается")
    INTERNAL_SERVER_ERROR = (3, 500, "internal_server_error", "Произошла внутренняя серверная ошибка. Повторите запрос")
    ACCESS_DENIED = (4, 403, "access_denied", "Доступ к ресурсу запрещён")
    NOT_FOUND = (5, 404, "not_found", "Не найдено")
    NOT_ENOUGH_PARAMS = (6, 400, "not_enough_params", "Не все параметры были указаны в запросе")
    MODEL_IS_NOT_LOADED = (7, 500, "model_is_not_loaded", "Модель не была загружена, выполнение невозможно")


class ResponseScheme:
    @staticmethod
    def success(response_body: dict = None):
        if response_body is None:
            response_body = {}

        return jsonify({
            "status": True, "response": response_body, "timestamp": time()
        })

    @staticmethod
    def error(error_body: dict = None, error: Errors = None):
        if error_body is None:
            error_body = {}

        if error is None:
            error = Errors.DEFAULT_PARSE_ERROR

        error_code, http_code, error_id, error_text = error.value

        return jsonify({
            "status": False, "error": {
                "error_code": error_code,
                "error_id": error_id,
                "error_text": error_text,
                "error_body": error_body
            }, "timestamp": time()
        }), http_code
