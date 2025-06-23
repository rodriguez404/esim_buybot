import pycountry
import re
import asyncio
from tortoise import Tortoise
from database.models.esim_local import DataBase_LocalCountry, DataBase_LocalTariff
from api.esim_access import fetch
from config import ESIM

import logging


def parse_slug(slug: str):
    if any(suffix in slug for suffix in ("_End", "_nonhkip")):
        return None

    match = re.match(r"[A-Z]{2}[-_](?P<gb>[\d.]+)_(?P<days>\d+|Daily)$", slug)
    if not match:
        return None

    gb = float(match.group("gb"))
    days = 1 if match.group("days") == "Daily" else int(match.group("days"))
    return gb, days


COUNTRY_CODE_MAP = {country.alpha_2: country.name for country in pycountry.countries}


async def process_country(code: str, name: str, sem: asyncio.Semaphore):
    async with sem:
        try:
            data = await fetch(ESIM.API_PACKAGELIST_URL, payload={'locationCode': code})
            package_list = data.get('obj', {}).get('packageList', [])
        except Exception as e:
            logging.debug(f"❌ Ошибка при получении данных по {code}: {e}")
            return

        local_packages = [
            pkg for pkg in package_list
            if pkg.get("locationNetworkList")
               and len(pkg["locationNetworkList"]) == 1
               and pkg["locationNetworkList"][0].get("locationCode") == code
        ]
        if not local_packages:
            return

        country_obj, _ = await DataBase_LocalCountry.get_or_create(
            location_code=code,
            defaults={"location_name": name}
        )

        for pkg in local_packages:
            slug = pkg.get("slug")
            package_code=pkg.get("packageCode")
            price = pkg.get("price", 0) / 10000
            if not slug:
                logging.debug(f"⚠️ Пропущено: нет slug в пакете: {pkg.get('name')}")
                continue
            parsed = parse_slug(slug)
            if not parsed:
                logging.debug(f"⚠️ Пропущено: не удалось распарсить slug: {slug}")
                continue
            gb, days = parsed
            try:
                await DataBase_LocalTariff.create(
                    country=country_obj,
                    slug=slug,
                    package_code=package_code,
                    gb=gb,
                    days=days,
                    price=price
                )
            except Exception as e:
                logging.error(f"❌ Ошибка при создании тарифа {slug}: {e}", exc_info=True)


async def update_esim_packages_local():
    # Очистка старых данных
    await DataBase_LocalTariff.all().delete()
    await DataBase_LocalCountry.all().delete()

    # Семафор для ограничения одновременных fetch-запросов
    sem = asyncio.Semaphore(3)
    tasks = [process_country(code, name, sem) for code, name in COUNTRY_CODE_MAP.items()]

    # Запускаем все задачи параллельно с ограничением семафором
    await asyncio.gather(*tasks)

    # Сброс последовательностей при необходимости
    await reset_local_sequences()


async def reset_local_sequences():
    conn = Tortoise.get_connection("default")
    await conn.execute_query('ALTER SEQUENCE "esim_local_countries_id_seq" RESTART WITH 1;')
    await conn.execute_query('ALTER SEQUENCE "esim_local_tariffs_id_seq" RESTART WITH 1;')