import allure
import pytest
import logging
from datetime import datetime
from faker import Faker
import os
import platform
import subprocess
from importlib.metadata import version

# Проверяет наличие папки logs
logs_dir = ".//logs"
os.makedirs(logs_dir, exist_ok=True)

# level - уровень логов INFO
# filename - путь к логам
# filemode - режим доступа к логам (а - дозапись)
# format - формат отображения информации в логах (asctime - дата и время, levelname - уровень лога, lineno - номер строки, filename - имя файла, funcName - имя модуля (функции), message - текст сообщения)
# encoding - кодировка UTF-8
logging.basicConfig(level=logging.INFO, 
                    filename=f"{logs_dir}//{datetime.now().strftime('%d-%m-%Y')}.log",
                    filemode="a",
                    # format="%(asctime)s - %(levelname)s(%(lineno)d)-(%(filename)s)-(%(funcName)s) == %(message)s",
                    format="%(asctime)s - %(levelname)s %(filename)s->%(funcName)s = %(message)s",
                    encoding="UTF-8")

@pytest.fixture(scope="session", autouse=True)
def info_start_session():
    """Фикстура стартует один раз в начале запуска тестов (scope="session")
    """
    logging.info(f"\n====================================\n=======START NEW TEST SESSION=======\n====================================")
    # Добавление окружение для теста в Allure-отчет
    allure_dir = "allure-results"
    os.makedirs(allure_dir, exist_ok=True)
    env_file = os.path.join(allure_dir, "environment.properties")
    with allure.step(f"Получение версий используемых библиотек"):
        os_version = f"{platform.system()} {platform.version()}"
        python_version = f"{platform.python_version()}"
        try:
            allure_version = subprocess.run(['allure', '--version'], capture_output=True, text=True, check=True, shell=True)
            allure_version = allure_version.stdout.strip()
        except subprocess.CalledProcessError as e:
            allure_version = "Ошибка при выполнении команды: {e}"
        except FileNotFoundError:
            allure_version = "Allure не установлен или не добавлен в PATH"
        pytest_version = version("pytest")
        allure_pytest_version = version("allure-pytest")
        requests_version = version("requests")
        faker_version = version("faker")
        prettytable_version = version("prettytable")
        pydantic_version = version("pydantic")
    with allure.step(f"Запись окружения в файл '{env_file}'"):
        with open(env_file, "w") as file:
            file.write(f"OS={os_version}\n")
            file.write(f"Python={python_version}\n")
            file.write(f"Allure={allure_version}\n")
            file.write(f"Pytest={pytest_version}\n")
            file.write(f"Allure-pytest={allure_pytest_version}\n")
            file.write(f"Requests={requests_version}\n")
            file.write(f"Faker={faker_version}\n")
            file.write(f"PrettyTable={prettytable_version}\n")
            file.write(f"Pydantic={pydantic_version}\n")
    yield
    logging.info(f"\n====================================\n==========END TEST SESSION==========\n====================================")

# Генерация фейкового пользователя
@pytest.fixture(scope="function")
def genarate_user():
    """Создает фейковые данные для пользователя через библиотеку Faker

    Returns:
        JSON: Возвращает name и job
    """
    
    logging.info(f"Создаю фейковые данный 'name' и 'job'")
    fake = Faker()
    name = fake.name()
    job = fake.job()
    logging.info(f"Фейковое name: {name}; фейковое job: {job}")

    return {
        "name": name,
        "job": job
    }