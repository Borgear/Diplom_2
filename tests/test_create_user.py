import pytest
import allure
from helpers import Helpers
import data

@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.story("Регистрация нового уникального пользователя")
    @allure.title("Успешная регистрация уникального пользователя")
    def test_register_unique_user(self, api_client, unique_email):
        password = Helpers.generate_random_password()
        name = data.DEFAULT_USER_NAME
        response = api_client.register(unique_email, password, name)
        assert response.status_code == data.OK
        body = response.json()
        assert body[data.SUCCESS] is True
        # Email сервер может вернуть в нижнем регистре, сравниваем регистронезависимо
        assert body[data.USER][data.EMAIL].lower() == unique_email.lower()
        assert body[data.USER][data.NAME] == name
        assert data.ACCESS_TOKEN in body
        assert data.REFRESH_TOKEN in body
        api_client.delete_user(body[data.ACCESS_TOKEN])

    @allure.story("Повторная регистрация существующего пользователя")
    @allure.title("Попытка регистрации уже существующего пользователя")
    def test_register_existing_user(self, api_client, registered_user):
        password = Helpers.generate_random_password()
        name = data.DEFAULT_USER_NAME
        response = api_client.register(registered_user[data.EMAIL], password, name)
        assert response.status_code == data.FORBIDDEN
        body = response.json()
        assert body[data.SUCCESS] is False
        assert body[data.MESSAGE] == data.USER_ALREADY_EXISTS

    @allure.story("Регистрация с пропущенными обязательными полями")
    @allure.title("Регистрация не проходит при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_missing_required_field(self, api_client, missing_field):
        payload = Helpers.generate_payload_without_field(missing_field, name=data.DEFAULT_USER_NAME)
        with allure.step(f"Попытка регистрации без поля '{missing_field}'"):
            response = api_client.register_raw(payload)
        assert response.status_code == data.FORBIDDEN
        body = response.json()
        assert body[data.SUCCESS] is False
        assert body[data.MESSAGE] == data.REQUIRED_FIELDS_MISSING
    