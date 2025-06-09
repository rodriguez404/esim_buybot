import re
from tortoise import Tortoise
from database.models.esim_regional import DataBase_Region, DataBase_RegionalTariff, DataBase_RegionalCountry
from api.esim_access import fetch
from config import ESIM


def parse_slug(slug: str):
    match = re.match(r"(?P<code>[A-Z]+)-(?P<country_count>\d+)_+(?P<gb>[\d.]+)_(?P<days>\d+|Daily)", slug)
    if not match:
        return None

    code = match.group("code")
    country_count = int(match.group("country_count"))
    gb = float(match.group("gb"))
    days_raw = match.group("days")
    days = 1 if days_raw == "Daily" else int(days_raw)

    return code, country_count, gb, days

async def update_esim_packages_regional():
    # Очистка таблиц
    await DataBase_RegionalCountry.all().delete()
    await DataBase_RegionalTariff.all().delete()
    await DataBase_Region.all().delete()

    # Получаем региональные тарифы
    regional_data = await fetch(ESIM.API_PACKAGELIST_URL, payload={'locationCode': '!RG'})
    regional_packages = regional_data.get('obj', {}).get('packageList', [])

    # Получаем глобальные тарифы
    global_data = await fetch(ESIM.API_PACKAGELIST_URL, payload={'locationCode': '!GL'})
    global_packages = global_data.get('obj', {}).get('packageList', [])

    # Объединяем оба списка
    package_list = regional_packages + global_packages

    region_map = {}  # code -> Region object

    for package in package_list:
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

        code, country_count, gb, days = parsed

        # Получаем человекочитаемое имя региона + кол-во стран
        base_region_name = REGION_CODE_MAP.get(code, code)
        region_name = f"{base_region_name} {country_count}"

        # Создание региона, если его нет
        if region_name not in region_map:
            region_obj = await DataBase_Region.create(name=region_name)
            region_map[region_name] = region_obj
        else:
            region_obj = region_map[region_name]

        # Создание тарифа
        tariff_obj = await DataBase_RegionalTariff.create(
            region=region_obj,
            slug=slug,
            gb=gb,
            days=days,
            price=price
        )

        # Добавление стран
        for country in package.get("locationNetworkList", []):
            await DataBase_RegionalCountry.create(
                region=region_obj,
                tariff=tariff_obj,
                location_name=country.get("locationName", ""),
                location_code=country.get("locationCode", "")
            )

    await reset_region_sequences()

async def reset_region_sequences():
    conn = Tortoise.get_connection("default")
    await conn.execute_query('ALTER SEQUENCE "esim_regional_regions_id_seq" RESTART WITH 1;')
    await conn.execute_query('ALTER SEQUENCE "esim_regional_tariffs_id_seq" RESTART WITH 1;')
    await conn.execute_query('ALTER SEQUENCE "esim_regional_countries_id_seq" RESTART WITH 1;')


# Словарь региональных кодов и их названий
REGION_CODE_MAP = {
    "EU": "Europe",
    "SA": "South America",
    "NA": "North America",
    "AF": "Africa",
    "AS": "Asia",
    "ME": "Middle East",
    "CN": "China",
    "CB": "Caribbean",
    "CA": "Central Asia",
    "GL": "Global",
    "SEA": "Southeast Asia",
    "AUNZ": "Oceania",
    "SGMYTH": "Southeast Asia",
    "CNJPKR": "East Asia"
}