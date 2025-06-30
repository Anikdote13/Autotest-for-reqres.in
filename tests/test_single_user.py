import json
import logging
from math import log
from textwrap import indent
from venv import logger
import pytest
import allure
import base_requests
import config
import assertion
from allure_commons.types import AttachmentType
import base_helper

link_website = "https://reqres.in/"

@allure.link(link_website, name=f"Сайт API: {link_website}")
@allure.epic(f"Получение конкретного пользователя GET: {config.API_SINGLE_USER}")
@allure.feature("Позитивные проверки")
class TestPositiveCheck:

    @allure.story("Выполнение API c передачей ID пользователя")
    @allure.title("Выполнение API c передачей ID пользователя")
    @allure.description("Возвращается информация по конкретному пользователю")
    @pytest.mark.parametrize("id", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    def test_get_users_with_id(self, id):

        response = base_requests.get_request(config.API_SINGLE_USER + id)

        assertion.assert_response(int(id), response.json()["data"]["id"], response=response, message=f"Сравниваю id пользователя 'id'")
        assertion.assert_status_code(200, response)

    @allure.story("Сравнение всех полей для всех пользователей")
    @allure.title("Сравнение всех полей для всех пользователей")
    def test_all_users(self):
        
        with allure.step(f"Получаю общее кол-во страниц с пользователями"):
            logging.info(f"Получаю общее кол-во страниц с пользователями")
            list_users = base_helper.get_list_users()
            total_pages = list_users.json()["total_pages"]
            logging.info(f"Всего страниц с пользователями: {total_pages}")
        
        with allure.step(f"Прохожусь по каждому пользователю и сравниваю поля"):
            for page in range(total_pages):
                with allure.step(f"Страница: {page + 1}"):
                    list_users = base_helper.get_list_users(page + 1)
                    base_helper.beautiful_table(response=list_users.json()["data"], message=f"Таблица пользователей для страницы № {page + 1}")
                    for users in list_users.json()["data"]:
                        with allure.step(f"Пользователь с id: {users["id"]}"):
                            info_user = base_helper.get_info_user(users["id"])
                            assertion.assert_response(users["id"], info_user.json()["data"]["id"], response=info_user, message=f"Сравниваю поле 'id'")
                            assertion.assert_response(users["email"], info_user.json()["data"]["email"], response=info_user, message=f"Сравниваю поле 'email'")
                            assertion.assert_response(users["first_name"], info_user.json()["data"]["first_name"], response=info_user, message=f"Сравниваю поле 'first_name'")
                            assertion.assert_response(users["last_name"], info_user.json()["data"]["last_name"], response=info_user, message=f"Сравниваю поле 'last_name'")
                            assertion.assert_response(users["avatar"], info_user.json()["data"]["avatar"], response=info_user, message=f"Сравниваю поле 'avatar'")
                            assertion.assert_status_code(200, info_user)



@allure.link(link_website, name=f"Сайт API: {link_website}")
@allure.epic(f"Получение конкретного пользователя GET: {config.API_SINGLE_USER}")
@allure.feature("Негативные проверки")
class TestNegativeCheck:


    @allure.title("Выполнение API без передачи ID пользователя")
    @allure.description("Возвращается информация о пользователях на первой странице")
    def test_get_users_without_id(self):

        response = base_requests.get_request(config.API_SINGLE_USER)

        assertion.assert_response(1, response.json()["page"], response=response, message=f"Сравниваю номер страницы 'page'")
        assertion.assert_status_code(200, response)

    @allure.title("Выполнение API с передачей нулевого ID пользователя")
    @allure.description("Возвращается пустой ответ")
    def test_get_users_with_id_equal_zero(self):

        response = base_requests.get_request(config.API_SINGLE_USER + "0")

        assertion.assert_response("{}", str(response.json()), response=response, message=f"Информация о пользователях пустая")
        assertion.assert_status_code(404, response)

    @allure.story("Выполнение API с передачей отрицательного ID пользователя")
    @allure.title("Выполнение API с передачей отрицательного ID пользователя")
    @allure.description("Возвращается пустой ответ")
    @pytest.mark.parametrize("id", ["-1", "-2", "-10", "-934234"])
    def test_get_users_with_minus_id(self, id):

        response = base_requests.get_request(config.API_SINGLE_USER + id)

        assertion.assert_response("{}", str(response.json()), response=response, message=f"Информация о пользователях пустая")
        assertion.assert_status_code(404, response)

    @allure.story("Выполнение API с передачей некорректного ID пользователя")
    @allure.title("Выполнение API с передачей некорректного ID пользователя")
    @allure.description("Возвращается пустой ответ")
    @pytest.mark.parametrize("id", ["test", "test123", "@#$%^&*()", "1test", "test1", "2test2"])
    def test_get_users_with_incorrect_id(self, id):

        response = base_requests.get_request(config.API_SINGLE_USER + id)

        assertion.assert_response("{}", str(response.json()), response=response, message=f"Информация о пользователях пустая")
        assertion.assert_status_code(404, response)