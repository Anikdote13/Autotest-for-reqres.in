import pytest
import allure
import base_requests
import config
import assertion
import base_helper


@allure.link(config.LINK_WEBSITE, name=f"Сайт API: {config.LINK_WEBSITE}")
@allure.epic(f"Получение списка пользователей GET: {config.API_LIST_USER}")
@allure.feature("Позитивные проверки")
class TestPositiveCheck:
    
    @allure.title("Выполнение API без передачи номера страницы")
    @allure.description("Возвращает данные о пользователях на первой странице")
    def test_get_list_users(self):

        response = base_requests.get_request(config.API_LIST_USER)

        base_helper.beautiful_table(response.json()["data"], message=f"Данные о пользователях в виде таблицы")
        assertion.assert_response(1, response.json()["page"], response=response, message=f"Сравниваю номер страницы 'page'")
        assertion.assert_status_code(200, response)

    @allure.story("Выполнение API с передачей номера страницы")
    @allure.title("Выполнение API с передачей номера страницы")
    @allure.description("Возвращает данные о пользователях на конкретной странице")
    @pytest.mark.parametrize("page", [1, 2, 3])
    def test_get_list_users_with_page(self, page):

        payload = {
            "page": page
        }

        response = base_requests.get_request(config.API_LIST_USER, payload=payload)

        assertion.assert_response(page, response.json()["page"], response=response, message=f"Вернулся передаваемый номер страницы 'page'")
        assertion.assert_status_code(200, response)

@allure.link(config.LINK_WEBSITE, name=f"Сайт API: {config.LINK_WEBSITE}")
@allure.epic(f"Получение списка пользователей GET: {config.API_LIST_USER}")
@allure.feature("Негативные проверки")
class TestNegativeCheck:

    @allure.story("Выполнение API с передачей некорректного номера страницы")
    @allure.title("Выполнение API с передачей некорректного номера страницы")
    @allure.description("Возвращает информацию о пользователях на первой странице")
    @pytest.mark.parametrize("page", ["test", "test123", "!@#$%^&*()_+", "1test2"])
    def test_get_list_users_with_incorrect_page(self, page):

        payload = {
            "page": page
        }

        response = base_requests.get_request(config.API_LIST_USER, payload=payload)

        assertion.assert_response(1, response.json()["page"], response=response, message=f"Сравниваю номер страницы 'page'")
        assertion.assert_status_code(200, response)

    @allure.story("Выполнение API с передачей несуществующего номера страницы")
    @allure.title("Выполнение API с передачей несуществующего номера страницы")
    @allure.description("Возвращает пустую информацию о пользователях")
    @pytest.mark.parametrize("page", [100, 9999, 345256346, 21345676534])
    def test_get_list_users_with_no_exists_page(self, page):

        payload = {
            "page": page
        }

        response = base_requests.get_request(config.API_LIST_USER, payload=payload)

        assertion.assert_response(page, response.json()["page"], response=response, message=f"Вернулся передаваемый номер страницы 'page'")
        assertion.assert_response("[]", str(response.json()["data"]), response=response, message=f"Информация о пользователях пустая ('data' пустая)")
        assertion.assert_status_code(200, response)

    @allure.story("Выполнение API с передачей отрицательного номера страницы")
    @allure.title("Выполнение API с передачей отрицательного номера страницы")
    @allure.description("Возвращает не всегда пустую информацию о пользователях")
    @pytest.mark.parametrize("page", [-1, -2, -10, -732786325])
    def test_get_list_users_with_minus_page(self, page):

        payload = {
            "page": page
        }

        response = base_requests.get_request(config.API_LIST_USER, payload=payload)

        assertion.assert_response(page, response.json()["page"], response=response, message=f"Вернулся передаваемый номер страницы 'page'")
        assertion.assert_status_code(200, response)

    @allure.title("Выполнение API с передачей нулевого номера страницы")
    @allure.description("Возвращает информацию о пользователях на первой странице")
    def test_get_list_users_with_zero_page(self):

        payload = {
            "page": 0
        }

        response = base_requests.get_request(config.API_LIST_USER, payload=payload)

        assertion.assert_response(1, response.json()["page"], response=response, message=f"Сравниваю номер страницы 'page'")
        assertion.assert_status_code(200, response)