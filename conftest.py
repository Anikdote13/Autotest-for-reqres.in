import pytest
import logging
from datetime import datetime
import random
from faker import Faker
import os

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
                    format="%(asctime)s - %(levelname)s(%(lineno)d)-(%(filename)s)-(%(funcName)s) == %(message)s",
                    encoding="UTF-8")

@pytest.fixture(scope="session", autouse=True)
def info_start_session():
    """Фикстура стартует один раз в начале запуска тестов (scope="session")
    """
    logging.info(f"\n====================================\n=======START NEW TEST SESSION=======\n====================================")
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