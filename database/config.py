from config import DATABASE

DB_CONFIG = {
    "connections": {
        "default": DATABASE.HOST
    },
    "apps": {
        "models": {
            "models": ["database.models.user", "database.models.esim_global", 'database.models.esim_regional', "aerich.models"],  # Подключаем модели
            "default_connection": "default",
        }
    }
}