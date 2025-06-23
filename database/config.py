from config import DATABASE

DB_CONFIG = {
    "connections": {
        "default": DATABASE.HOST
    },
    "apps": {
        "models": {
            "models": ["database.models.user", 
                       "database.models.esim_regional_and_global", 
                       "database.models.esim_local", 
                       "database.models.admin_tariff_groups", 
                       "aerich.models"
                       ],  # Подключаем модели
            "default_connection": "default",
        }
    }
}