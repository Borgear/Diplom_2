import allure
import data
from helpers import Helpers

@allure.feature("Вход пользователя")
@allure.story("Вход с корректными учётными данными")
@allure.title("Успешный вход под существующим пользователем")
def test_login_existing_user(api_client, registered_user):
    response = api_client.login(registered_user[data.EMAIL], registered_user["password"])
    assert response.status_code == data.OK
    body = response.json()
    assert body[data.SUCCESS] is True
    assert data.ACCESS_TOKEN in body
    assert data.REFRESH_TOKEN in body
    assert body[data.USER][data.EMAIL] == registered_user[data.EMAIL]

@allure.feature("Вход пользователя")
@allure.story("Вход с неверным паролем")
@allure.title("Вход не удаётся с неправильным паролем")
def test_login_wrong_password(api_client, registered_user):
    password = Helpers.generate_random_password()
    response = api_client.login(registered_user[data.EMAIL], password)
    assert response.status_code == data.UNAUTHORIZED
    body = response.json()
    assert body[data.SUCCESS] is False
    assert body[data.MESSAGE] == data.INVALID_CREDENTIALS

@allure.feature("Вход пользователя")
@allure.story("Вход с несуществующим email")
@allure.title("Вход не удаётся для неизвестного пользователя")
def test_login_nonexistent_email(api_client, unique_email):
    password = Helpers.generate_random_password()
    response = api_client.login(unique_email, password)
    assert response.status_code == data.UNAUTHORIZED
    body = response.json()
    assert body[data.SUCCESS] is False
    assert body[data.MESSAGE] == data.INVALID_CREDENTIALS
    