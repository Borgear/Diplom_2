import allure
import data

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Создание заказа с авторизацией и валидными ингредиентами")
    @allure.title("Успешное создание заказа авторизованным пользователем")
    def test_create_order_with_auth(self, api_client, registered_user, valid_ingredients):
        assert len(valid_ingredients) >= 2, "Нужно как минимум два ингредиента"
        response = api_client.create_order(valid_ingredients, token=registered_user[data.ACCESS_TOKEN])
        assert response.status_code == data.OK
        body = response.json()
        assert body[data.SUCCESS] is True
        assert data.ORDER in body
        assert data.NUMBER in body[data.ORDER]

    @allure.story("Создание заказа без авторизации")
    @allure.title("Создание заказа не проходит без токена авторизации")
    def test_create_order_without_auth(self, api_client, valid_ingredients):
        response = api_client.create_order(valid_ingredients)  
        assert response.status_code in (data.UNAUTHORIZED, data.FORBIDDEN)
        body = response.json()
        assert body[data.SUCCESS] is False
        assert body[data.MESSAGE] == data.NOT_AUTHORISED_MESSAGE

    @allure.story("Создание заказа с пустым списком ингредиентов")
    @allure.title("Заказ не создаётся, если не переданы ингредиенты")
    def test_create_order_without_ingredients(self, api_client, registered_user):
        response = api_client.create_order([], token=registered_user[data.ACCESS_TOKEN])
        assert response.status_code == data.BAD_REQUEST
        body = response.json()
        assert body[data.SUCCESS] is False
        assert body[data.MESSAGE] == data.INGREDIENTS_NOT_PROVIDED

    @allure.story("Создание заказа с невалидным хешем ингредиента")
    @allure.title("Заказ не создаётся с несуществующим ID ингредиента")
    def test_create_order_invalid_hash(self, api_client, registered_user):
        response = api_client.create_order([data.INVALID_INGREDIENT_HASH], token=registered_user[data.ACCESS_TOKEN])
        assert response.status_code == data.INTERNAL_SERVER_ERROR
