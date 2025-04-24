import re

from tortoise import Tortoise

from database.models.esim_global import DataBase_EsimPackageGlobal, DataBase_EsimCountryGlobal

from api.esim_access import fetch, url_packagelist

async def updata_esim_packages_global():
    await DataBase_EsimPackageGlobal.all().delete()
    await DataBase_EsimCountryGlobal.all().delete()

    data = await fetch(url_packagelist, payload={'locationCode': '!GL'})
    package_list = data.get('obj', {}).get('packageList', [])

    for package in package_list:
        name = package.get("name", "")
        price = package.get("price", 0) // 10000

        # Пытаемся извлечь GB и Days
        try:
            gb = int(re.search(r"(\d+)GB", name).group(1))
            days = int(re.search(r"(\d+)Days", name).group(1))
        except Exception as e:
            print(f"⚠️ Не удалось распарсить тариф: {name}, ошибка: {e}")
            continue

        # Сохраняем только очищенные данные
        esim_package = await DataBase_EsimPackageGlobal.create(gb=gb, days=days, price=price)

        for country in package.get("locationNetworkList", []):
            await DataBase_EsimCountryGlobal.create(
                package=esim_package,
                location_name=country["locationName"],
                location_code=country["locationCode"]
            )

    await reset_sequence()

async def reset_sequence():
    conn = Tortoise.get_connection("default")
    await conn.execute_query('ALTER SEQUENCE esim_package_global_id_seq RESTART WITH 1;')
    await conn.execute_query('ALTER SEQUENCE esim_countries_global_id_seq RESTART WITH 1;')
