import pycountry
import re
from tortoise import Tortoise
from database.models.esim_local import DataBase_LocalCountry, DataBase_LocalTariff
from api.esim_access import fetch, url_packagelist


def parse_slug(slug: str):
    if any(suffix in slug for suffix in ["_End", "_nonhkip"]):
        return None

    match = re.match(r"[A-Z]{2}[-_](?P<gb>[\d.]+)_(?P<days>\d+|Daily)$", slug)
    if not match:
        return None

    gb = float(match.group("gb"))
    days_raw = match.group("days")
    days = 1 if days_raw == "Daily" else int(days_raw)

    return gb, days


# Основная версия
async def update_esim_packages_local():
    await DataBase_LocalTariff.all().delete()
    await DataBase_LocalCountry.all().delete()

    for country_code, country_name in COUNTRY_CODE_MAP.items():
        try:
            data = await fetch(url_packagelist, payload={'locationCode': country_code})
            package_list = data.get('obj', {}).get('packageList', [])
        except Exception as e:
            print(f"❌ Ошибка при получении данных по {country_code}: {e}")
            continue

        local_packages = [
            pkg for pkg in package_list
            if pkg.get("locationNetworkList") and
               len(pkg["locationNetworkList"]) == 1 and
               pkg["locationNetworkList"][0].get("locationCode") == country_code
        ]

        if not local_packages:
            continue

        country_obj, _ = await DataBase_LocalCountry.get_or_create(
            location_code=country_code,
            defaults={"location_name": country_name}
        )

        for package in local_packages:
            slug = package.get("slug")
            price = package.get("price", 0) / 10000
            package_code = package.get("packageCode", "")

            if not slug:
                print(f"⚠️ Пропущено: нет slug в пакете: {package.get('name')}")
                continue

            parsed = parse_slug(slug)
            if not parsed:
                print(f"⚠️ Пропущено: не удалось распарсить slug: {slug}")
                continue

            gb, days = parsed

            country_obj, _ = await DataBase_LocalCountry.get_or_create(
                location_code=country_code,
                defaults={"location_name": country_name}
            )

            await DataBase_LocalTariff.create(
                country=country_obj,
                package_code=package_code,
                gb=gb,
                days=days,
                price=price
            )

    await reset_local_sequences()


async def reset_local_sequences():
    conn = Tortoise.get_connection("default")
    await conn.execute_query('ALTER SEQUENCE "esim_local_countries_id_seq" RESTART WITH 1;')
    await conn.execute_query('ALTER SEQUENCE "esim_local_tariffs_id_seq" RESTART WITH 1;')


# Общий мап стран
COUNTRY_CODE_MAP = {
    country.alpha_2: country.name for country in pycountry.countries
}