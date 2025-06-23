from database.services.esim_service_local import update_esim_packages_local
from database.services.esim_service_regional_and_global import update_esim_packages_regional
from redis_folder.functions.set_static_cache import set_static_cache

import logging

async def update_all_packages():
    try:
        logging.info("🏠 Обновление локальных пакетов...")
        await update_esim_packages_local()

        logging.info("🌍 Обновление региональных пакетов...")
        await update_esim_packages_regional()

        logging.info("🧠 Обновление Redis кэша...")
        await set_static_cache()

        logging.info("✅ Обновление завершено успешно.")
    except Exception as e:
        logging.debug(f"❌ Ошибка во время обновления: {e}")