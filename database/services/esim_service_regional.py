import re
from tortoise import Tortoise
from database.models.esim_regional import DataBase_Region, DataBase_RegionalTariff, DataBase_RegionalCountry
from api.esim_access import fetch, url_packagelist


def parse_slug(slug: str):
    match = re.match(r"(?P<code>[A-Z]+)-\d+_(?P<gb>[\d.]+)_(?P<days>\d+|Daily)", slug)
    if not match:
        return None

    code = match.group("code")
    gb = float(match.group("gb"))
    days_raw = match.group("days")
    days = 1 if days_raw == "Daily" else int(days_raw)

    return code, gb, days

async def update_esim_packages_regional():
    # Очистка таблиц
    await DataBase_RegionalCountry.all().delete()
    await DataBase_RegionalTariff.all().delete()
    await DataBase_Region.all().delete()

    data = await fetch(url_packagelist, payload={'locationCode': '!RG'})
    package_list = data.get('obj', {}).get('packageList', [])

    region_map = {}  # code -> Region object

    for package in package_list:
        slug = package.get("slug")
        price = package.get("price", 0) / 10000

        if not slug:
            print(f"⚠️ Пропущено: нет slug в пакете: {package.get('name')}")
            continue

        parsed = parse_slug(slug)
        if not parsed:
            print(f"⚠️ Пропущено: не удалось распарсить slug: {slug}")
            continue

        code, gb, days = parsed
        region_name = REGION_CODE_MAP.get(code, code)  # используем map, если нет — оставляем код

        # Создание региона, если его нет
        if code not in region_map:
            region_obj = await DataBase_Region.create(name=region_name)
            region_map[code] = region_obj
        else:
            region_obj = region_map[code]

        # Создание тарифа
        tariff_obj = await DataBase_RegionalTariff.create(
            region=region_obj,
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
    "SGMYTH": "Southeast Asia",
    "CNJPKR": "East Asia"
}