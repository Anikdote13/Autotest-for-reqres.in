import logging
import base_requests
import config
from prettytable import PrettyTable
import json
import allure
from allure_commons.types import AttachmentType

def get_list_users(page=None):
    """Получает список всех пользователей

    Args:
        page (int, optional): Конкретная страница с которой получить список пользователей. Defaults to None.

    Returns:
        JSON: Возвращает список пользователей
    """

    payload = {
        "page": page
    }

    response = base_requests.get_request(config.API_LIST_USER, payload=payload)

    return response

def get_info_user(id):
    """Получает информацию по конкретному пользователю

    Args:
        id (int, optional): ID конкретного пользователя. Defaults to None.

    Returns:
        JSON: Возвращает информацию по пользователю
    """

    response = base_requests.get_request(config.API_SINGLE_USER + str(id))

    return response

def beautiful_table(response, message="Таблица с данными"):
    """Преобразует переданный JSON в таблицу.\n
    JSON ключи - названия столбцов\n
    JSON значения - данные в строке

    Args:
        response (JSON): JSON, который нужно преобразовать
        message (str, optional): Дополнительное информационное сообщение. Defaults to "Таблица с данными".
    """

    # Создаем таблицу и добавляем в нее названия столбцов
    table = PrettyTable()
    table.field_names = response[0].keys()

    # Добавляем даныне в таблицу
    for item in response:
        table.add_row(item.values())

    with allure.step(message):
        allure.attach(body=str(table), name="Table", attachment_type=AttachmentType.TEXT)
        logging.info(f"\n{table}")

def attach_api(response, payload=None):
    """Прикрепляет информацию об API (запрос/ответ) к allure отчету

    Args:
        response (any): Данные об API
        payload (any): Отправляемые данные АПИ. Defaults to None.
    """

    allure.attach(response.url, name="API request", attachment_type=AttachmentType.JSON)
    allure.attach(body=json.dumps(payload, indent=4), name="API payload", attachment_type=AttachmentType.JSON)
    allure.attach(body=json.dumps(response.json(), indent=4), name="API response", attachment_type=AttachmentType.JSON)
    allure.attach(body=str(response.status_code), name="API response status code", attachment_type=AttachmentType.TEXT)
