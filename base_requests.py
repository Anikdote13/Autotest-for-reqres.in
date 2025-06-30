import logging
import pytest
import allure
import requests
from allure_commons.types import AttachmentType
import config
import json
import base_helper

def get_request(url, payload=None):
    """Выполнить GET запрос с/без параметров

    Args:
        url (str): URL API
        payload (JSON, optional): Параметры запроса. По умолчанию None.

    Returns:
        JSON: Возвращает JSON ответ от API
    """

    with allure.step(f"Выполняю GET запрос"):
        logging.info(f"GET запрос. {url}. Параметры: {payload}")
        response = requests.get(url, params=payload, headers=config.HEADERS)
        logging.info(f"Ответ на запрос: {response.url}")
        logging.info(f"Тело ответа: {response.text}")
        logging.info(f"Статуc код ответа: {response.status_code}")
        base_helper.attach_api(response=response, payload=payload)

    return response

def post_request(url, payload=None):    
    """Выполнить POST запрос с/без тела запроса

    Args:
        url (str): URL API
        payload (JSON, optional): Тело запроса. По умолчанию None
    """

    with allure.step(f"Выполняю POST запрос"):
        logging.info(f"POST запрос. {url}. Тело: {payload}")
        response = requests.post(url, json=payload, headers=config.HEADERS)
        logging.info(f"Ответ на запрос: {response.url}")
        logging.info(f"Тело ответа: {response.text}")
        logging.info(f"Статуc код ответа: {response.status_code}")
        base_helper.attach_api(response=response, payload=payload)

    return response