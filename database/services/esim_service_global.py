import re

from tortoise import Tortoise

from database.models.esim_global import DataBase_EsimPackageGlobal, DataBase_EsimCountryGlobal

from api.esim_access import fetch

from config import ESIM

import logging

async def update_esim_packages_global():
    await DataBase_EsimPackageGlobal.all().delete()
    await DataBase_EsimCountryGlobal.all().delete()

    data = await fetch(ESIM.API_PACKAGELIST_URL, payload={'locationCode': '!GL'})
    package_list = data.get('obj', {}).get('packageList', [])

    for package in package_list:
        name = package.get("name", "")
        price = package.get("price", 0) / 10000
        package_code = package.get("packageCode", "")

        # Пытаемся извлечь GB и Days
        try:
            gb = float(re.search(r"(\d+)GB", name).group(1))
            days = int(re.search(r"(\d+)Days", name).group(1))
        except Exception as e:
            logging.debug(f"⚠️ Не удалось распарсить тариф: {name}, ошибка: {e}")
            continue

        # Сохраняем только очищенные данные
        esim_package = await DataBase_EsimPackageGlobal.create(package_code=package_code, gb=gb, days=days, price=price)

        for country in package.get("locationNetworkList", []):
            await DataBase_EsimCountryGlobal.create(
                package=esim_package,
                location_name=country["locationName"],
                location_code=country["locationCode"]
            )

    await reset_sequence()

async def reset_sequence():
    conn = Tortoise.get_connection("default")
    await conn.execute_query('ALTER SEQUENCE esim_global_package_id_seq RESTART WITH 1;')
    await conn.execute_query('ALTER SEQUENCE esim_global_countries_id_seq RESTART WITH 1;')
