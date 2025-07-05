import json
import logging

from database.functions import esim_lists
from redis_folder.redis_client import get_redis
from config import SUPPORTED_LANGUAGES
from redis_folder.redis_mock_class import AsyncDummyRedis

# Для отладки
import time


async def set_static_cache():
    """
    Кэшируется с БД, не с API напрямую
    Статичный кэш обновляется сразу после обновления БД
    На данный момент кэшируется:
    - Список всех стран по каждому языку (Местные eSIM)
    - Список регионов по каждому языку (Региональные eSIM)
    - Международные тарифы (Международные eSIM)
    """
    # Сразу выйти с функции, если редис не активен
    if isinstance(get_redis(), AsyncDummyRedis):
        return
    
    logging.info("Обновление Кэша REDIS")
    
    # Для отладки - начало таймера для замера времени записи кэша
    start_total_time = time.time()

    # Глобальные eSIM: тарифы
    # start_global_time = time.time()
    # await get_redis().set(f"esim_global", json.dumps(await esim_lists.esim_regional()))

    # duration = (time.time() - start_global_time) * 1000  # в мс
    # logging.debug(f"[CACHE] Кэш esim_global обновлён за {duration:.2f} мс")

    # Кэш по всем языкам
    start_local_countries_time = {}
    start_regional_regions_time = {}
    for lang in SUPPORTED_LANGUAGES:
        # Локальные eSIM: названия стран
        start_local_countries_time[lang] = time.time()
        await get_redis().set(f"esim_local_countries_{lang}", json.dumps(await esim_lists.esim_local_countries(lang)))
        duration = (time.time() - start_local_countries_time[lang]) * 1000  # в мс
        logging.debug(f": [CACHE] Кэш esim_local_countries_{lang} обновлён за {duration:.2f} мс")

        # Региональные eSIM: названия регионов
        start_regional_regions_time[lang] = time.time()
        await get_redis().set(f"esim_regional_regions_{lang}", json.dumps(await esim_lists.esim_regional(lang)))
        duration = (time.time() - start_regional_regions_time[lang]) * 1000  # в мс
        logging.debug(f"[CACHE] Кэш esim_regional_regions_{lang} обновлён за {duration:.2f} мс")

    duration = (time.time() - start_total_time) * 1000  # в мс
    logging.debug(f"[CACHE] Суммарное время обновления кэша: {duration:.2f} мс")
    return


