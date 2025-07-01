import pytest
import allure
import base_requests
import config
import assertion
from datetime import datetime


@allure.link(config.LINK_WEBSITE, name=f"Сайт API: {config.LINK_WEBSITE}")
@allure.epic(f"Создание пользователя POST: {config.API_CREATE_USER}")
@allure.feature("Позитивные проверки")
class TestPositiveCheck:
    
    @allure.story("Выполнение API с передачей всех полей")
    @allure.title("Выполнение API с передачей всех полей")
    @allure.description(f"Возвращает данные о созданном пользователе")
    @pytest.mark.parametrize("iteration", range(5))
    def test_create_user(self, iteration, genarate_user):

        name = genarate_user["name"]
        job = genarate_user["job"]
        allure.dynamic.parameter(name="name", value=name)
        allure.dynamic.parameter(name="job", value=job)

        payload = {
            "name": name,
            "job": job
        }

        response = base_requests.post_request(config.API_CREATE_USER, payload=payload)

        assertion.assert_response(name, response.json()["name"], response=response, message=f"Сравниваю поле 'name'")
        assertion.assert_response(job, response.json()["job"], response=response, message=f"Сравниваю поле 'job'")
        assertion.assert_response(datetime.now().strftime("%Y-%m-%d"), response.json()["createdAt"][:10], response=response, message=f"Сравниваю поле 'createdAt'")
        assertion.assert_status_code(201, response)

    @allure.story("Выполнение API с передачей только поля 'name'")
    @allure.title("Выполнение API с передачей только поля 'name'")
    @allure.description(f"Возвращает только 'name' созданного пользователя")
    @pytest.mark.parametrize("iteration", range(5))
    def test_create_user_only_field_name(self, iteration, genarate_user):

        name = genarate_user["name"]
        allure.dynamic.parameter(name="name", value=name)

        payload = {
            "name": name
        }

        response = base_requests.post_request(config.API_CREATE_USER, payload=payload)

        assertion.assert_response(name, response.json()["name"], response=response, message=f"Сравниваю поле 'name'")
        assertion.assert_response(datetime.now().strftime("%Y-%m-%d"), response.json()["createdAt"][:10], response=response, message=f"Сравниваю поле 'createdAt'")
        assertion.assert_status_code(201, response)

    @allure.story("Выполнение API с передачей только поля 'job'")
    @allure.title("Выполнение API с передачей только поля 'job'")
    @allure.description(f"Возвращает только 'job' созданного пользователя")
    @pytest.mark.parametrize("iteration", range(5))
    def test_create_user_only_field_job(self, iteration, genarate_user):

        job = genarate_user["job"]
        allure.dynamic.parameter(name="job", value=job)

        payload = {
            "job": job
        }

        response = base_requests.post_request(config.API_CREATE_USER, payload=payload)

        assertion.assert_response(job, response.json()["job"], response=response, message=f"Сравниваю поле 'job'")
        assertion.assert_response(datetime.now().strftime("%Y-%m-%d"), response.json()["createdAt"][:10], response=response, message=f"Сравниваю поле 'createdAt'")
        assertion.assert_status_code(201, response)

    @allure.title("Выполнение API без передачи полей")
    @allure.description(f"Возвращает только дату создания пользователя")
    def test_create_user_without_field(self):

        response = base_requests.post_request(config.API_CREATE_USER)

        assertion.assert_response(datetime.now().strftime("%Y-%m-%d"), response.json()["createdAt"][:10], response=response, message=f"Сравниваю поле 'createdAt'")
        assertion.assert_status_code(201, response)

@allure.link(config.LINK_WEBSITE, name=f"Сайт API: {config.LINK_WEBSITE}")
@allure.epic(f"Создание пользователя POST: {config.API_CREATE_USER}")
@allure.feature("Негативные проверки")
class TestNegativeCheck:


    @allure.title("Выполнение API с передачей несуществующего поля")
    @allure.description(f"Возвращает несуществующее поле")
    def test_create_user_only_field_name(self):

        payload = {
            "test1": "test1"
        }

        response = base_requests.post_request(config.API_CREATE_USER, payload=payload)

        assertion.assert_response("test1", response.json()["test1"], response=response, message=f"Сравниваю переданное несуществующее поле")
        assertion.assert_response(datetime.now().strftime("%Y-%m-%d"), response.json()["createdAt"][:10], response=response, message=f"Сравниваю поле 'createdAt'")
        assertion.assert_status_code(201, response)