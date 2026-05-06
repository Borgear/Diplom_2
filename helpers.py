import random
import string

class Helpers: # Вспомогательные статические методы для генерации тестовых данных.

    @staticmethod
    def generate_unique_email(): # Генерирует email по шаблону: dmitry_baryshev_41_3цифры@yandex.ru
        digits = random.randint(100, 999)
        return f"dmitry_baryshev_41_{digits}@yandex.ru"

    @staticmethod
    def generate_random_password(length=8): # Генерирует случайный пароль заданной длины из строчных букв и цифр.
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    @staticmethod
    def generate_payload_without_field(missing_field: str, name: str = "Алекс") -> dict: # Создаёт корректный payload для регистрации, но без указанного поля.
        email = Helpers.generate_unique_email()
        password = Helpers.generate_random_password()
        payload = {"email": email, "password": password, "name": name}
        payload.pop(missing_field, None)
        return payload
    