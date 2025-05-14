from database.services.esim_service_local import update_esim_packages_local
from database.services.esim_service_regional import update_esim_packages_regional
from database.services.esim_service_global import update_esim_packages_global
from redis_folder.functions.set_static_cache import set_static_cache


async def update_all_packages():
    try:
        print("🏠 Обновление локальных пакетов...")
        await update_esim_packages_local()

        print("🌍 Обновление региональных пакетов...")
        await update_esim_packages_regional()

        print("📦 Обновление глобальных пакетов...")
        await update_esim_packages_global()


        print("🧠 Обновление Redis кэша...")
        await set_static_cache()

        print("✅ Обновление завершено успешно.")
    except Exception as e:
        print(f"❌ Ошибка во время обновления: {e}")