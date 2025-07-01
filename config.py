BASE_URL = f"https://reqres.in"
API_LIST_USER = f"{BASE_URL}/api/users" # Получение списка пользователей
API_SINGLE_USER = f"{BASE_URL}/api/users/" # Получние конкретного пользователя по ID
API_CREATE_USER = f"{BASE_URL}/api/users" # Создание пользователя

HEADERS = {
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'x-api-key': 'reqres-free-v1'
}

LINK_WEBSITE = "https://reqres.in/"