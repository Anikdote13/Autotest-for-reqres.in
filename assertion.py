from email import message
import logging
import pytest
import allure
import json
from allure_commons.types import AttachmentType
from pytest_check import check

@check.check_func # Что бы тест-не падал сразу после первой проверки и выполнил оставшиеся проверки
def assert_status_code(expected, response):
    """Проверка статус кода

    Args:
        expected (int): Ожидаемый статус код
        response (str): Ответ от API
    """

    # Строка для вывода сообщение об ожидаемом и фактических результатах
    assert_message = f"ОР статус код: {expected} ; ФР статус код: {response.status_code}"

    logging.info(assert_message)

    with allure.step(assert_message):
        allure.attach(body=json.dumps(response.json(), indent=4), name="API response", attachment_type=AttachmentType.JSON)
        assert expected == response.status_code, assert_message

@check.check_func # Что бы тест-не падал сразу после первой проверки и выполнил оставшиеся проверки
def assert_response(expected, actual, response, message=None):
    """Проверка тела ответа

    Args:
        expected (any): Ожидаемый результат
        actual (any): Фактический результат
        response (any): Ответ от API
        message (str, optional): Дополнительное сообщение для пояснения что сравнивается. Defaults to None.
    """

    # Строка для вывода сообщение об ожидаемом и фактических результатах
    if message==None:
        assert_message = f"ОР: {expected}; ФР: {actual}"
    else:
        assert_message = f"{message}. ОР: {expected}; ФР: {actual}"

    logging.info(assert_message)
    
    with allure.step(assert_message):
        allure.attach(body=json.dumps(response.json(), indent=4), name="API response", attachment_type=AttachmentType.JSON)
        assert expected == actual, assert_message