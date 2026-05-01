import requests
import allure
import json
from urls import Urls


class StellarBurgersAPI:
    def log_request_response(self, request_info: dict, response: requests.Response): # Внутренний метод: прикрепляет к Allure-отчёту информацию о запросе и теле ответа.
        allure.attach(
            json.dumps(request_info, indent=2, ensure_ascii=False),
            name="Запрос",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            response.text,
            name="Ответ",
            attachment_type=allure.attachment_type.TEXT
        )

    def register(self, email: str, password: str, name: str) -> requests.Response: # Регистрирует нового пользователя, передавая все обязательные поля.
        payload = {"email": email, "password": password, "name": name}
        url = f"{Urls.BASE_URL}{Urls.REGISTER_ENDPOINT}"
        with allure.step(f"POST {Urls.REGISTER_ENDPOINT} с email={email}"):
            response = requests.post(url, json=payload)
            self.log_request_response({"url": url, "payload": payload}, response)
        return response

    def register_raw(self, payload: dict) -> requests.Response: # Регистрирует пользователя с произвольным содержимым тела запроса.
        url = f"{Urls.BASE_URL}{Urls.REGISTER_ENDPOINT}"
        with allure.step(f"POST {Urls.REGISTER_ENDPOINT} с произвольным payload={payload}"):
            response = requests.post(url, json=payload)
            self.log_request_response({"url": url, "payload": payload}, response)
        return response

    def login(self, email: str, password: str) -> requests.Response: # Авторизует пользователя по email и паролю.
        payload = {"email": email, "password": password}
        url = f"{Urls.BASE_URL}{Urls.LOGIN_ENDPOINT}"
        with allure.step(f"POST {Urls.LOGIN_ENDPOINT} с email={email}"):
            response = requests.post(url, json=payload)
            self.log_request_response({"url": url, "payload": payload}, response)
        return response

    def get_ingredients(self) -> requests.Response: # Получает полный список доступных ингредиентов.
        url = f"{Urls.BASE_URL}{Urls.INGREDIENTS_ENDPOINT}"
        with allure.step(f"GET {Urls.INGREDIENTS_ENDPOINT}"):
            response = requests.get(url)
            self.log_request_response({"url": url}, response)
        return response

    def create_order(self, ingredients: list, token: str = None) -> requests.Response: # Создаёт заказ с указанными ингредиентами.
        headers = {}
        if token:
            headers["Authorization"] = token
        payload = {"ingredients": ingredients}
        url = f"{Urls.BASE_URL}{Urls.ORDERS_ENDPOINT}"
        with allure.step(f"POST {Urls.ORDERS_ENDPOINT} с ингредиентами={ingredients}"):
            response = requests.post(url, json=payload, headers=headers)
            self.log_request_response(
                {"url": url, "payload": payload, "headers": headers},
                response
            )
        return response

    def delete_user(self, token: str) -> requests.Response: # Удаляет пользователя.
        headers = {"Authorization": token}
        url = f"{Urls.BASE_URL}{Urls.USER_ENDPOINT}"
        with allure.step(f"DELETE {Urls.USER_ENDPOINT}"):
            response = requests.delete(url, headers=headers)
            self.log_request_response(
                {"url": url, "headers": headers},
                response
            )
        return response

    def get_user(self, token: str) -> requests.Response: # Возвращает данные текущего авторизованного пользователя.
        headers = {"Authorization": token}
        url = f"{Urls.BASE_URL}{Urls.USER_ENDPOINT}"
        with allure.step(f"GET {Urls.USER_ENDPOINT}"):
            response = requests.get(url, headers=headers)
            self.log_request_response(
                {"url": url, "headers": headers},
                response
            )
        return response
    