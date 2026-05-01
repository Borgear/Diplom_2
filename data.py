# HTTP‑статусы
OK = 200
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
INTERNAL_SERVER_ERROR = 500

# Сообщения об ошибках
USER_ALREADY_EXISTS = "User already exists"
REQUIRED_FIELDS_MISSING = "Email, password and name are required fields"
INVALID_CREDENTIALS = "email or password are incorrect"
INGREDIENTS_NOT_PROVIDED = "Ingredient ids must be provided"
NOT_AUTHORISED_MESSAGE = "You should be authorised"

# Ключи JSON‑ответов
SUCCESS = "success"
MESSAGE = "message"
USER = "user"
EMAIL = "email"
NAME = "name"
ACCESS_TOKEN = "accessToken"
REFRESH_TOKEN = "refreshToken"
ORDER = "order"
NUMBER = "number"
INGREDIENTS_DATA = "data"          

# Прочие константы
INVALID_INGREDIENT_HASH = "invalid_hash_12345"
FALLBACK_INGREDIENTS = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]
DEFAULT_USER_NAME = "Дмитрий"        
