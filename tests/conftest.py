import pytest
import requests
import allure
from api_object import StellarBurgersAPI
from helpers import Helpers
import data

@pytest.fixture(scope="function")
def api_client():
    return StellarBurgersAPI()

@pytest.fixture(scope="function")
def unique_email():
    return Helpers.generate_unique_email()

@pytest.fixture(scope="function")
def registered_user(api_client, unique_email): # Регистрирует нового пользователя со случайным паролем и именем по умолчанию. После теста удаляет пользователя.
    password = Helpers.generate_random_password()
    name = data.DEFAULT_USER_NAME
    response = api_client.register(unique_email, password, name)
    assert response.status_code == data.OK, f"Регистрация не удалась: {response.text}"
    assert response.json()[data.SUCCESS] is True

    user_data = {
        data.EMAIL: unique_email,
        "password": password,
        data.NAME: name,
        data.ACCESS_TOKEN: response.json()[data.ACCESS_TOKEN],
        data.REFRESH_TOKEN: response.json()[data.REFRESH_TOKEN]
    }
    yield user_data

    # Очистка с обработкой возможных ошибок
    try:
        api_client.delete_user(user_data[data.ACCESS_TOKEN])
    except Exception as e:
        allure.attach(
            str(e),
            name="Ошибка при удалении пользователя (очистка)",
            attachment_type=allure.attachment_type.TEXT
        )

@pytest.fixture(scope="function")
def valid_ingredients(api_client): # Фикстура, предоставляющая два валидных ID ингредиентов.
    try:
        response = api_client.get_ingredients()
        if response.status_code == data.OK and response.json()[data.SUCCESS]:
            ingr_list = response.json()[data.INGREDIENTS_DATA]
            if len(ingr_list) >= 2:
                return [ingr_list[0]["_id"], ingr_list[1]["_id"]]
    except requests.RequestException:
        pass
    return data.FALLBACK_INGREDIENTS
