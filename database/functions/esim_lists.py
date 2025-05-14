
from database.models.esim_local import DataBase_LocalCountry, DataBase_LocalTariff
from database.models.esim_global import DataBase_EsimCountryGlobal, DataBase_EsimPackageGlobal
from database.models.esim_regional import DataBase_Region, DataBase_RegionalCountry, DataBase_RegionalTariff

from microservices.format_number_UI import format_number
from microservices.code_to_flag import code_to_flag

from localization.localization import translate_countries, translate_regions

# Местные eSIM: страны
async def esim_local_countries(user_language):
    countries_list = []

    countries = await DataBase_LocalCountry.all()

    for country in countries:
        countries_list.append([country.id, translate_countries(country.location_name, user_language), code_to_flag(country.location_code)])

    # Сортировка по названию страны (по алфавиту)
    countries_list = sorted(countries_list, key=lambda x: x[1])

    return countries_list


# Местные eSIM: Конкретная страна -> тарифы
async def esim_local_selected_country_plans(country_id):
    plans = []

    packages = await DataBase_LocalTariff.filter(country=country_id).all()

    for package in packages:
        plans.append([package.id, format_number(package.gb), package.days, format_number(package.price)])

    # Сортировка: по объему, затем по количеству дней, затем по цене
    plans.sort(key=lambda x: (x[1], x[2], x[3]))

    return plans


# Региональные eSIM: регионы
async def esim_regional(user_language):
    plans = []

    packages = await DataBase_Region.all()

    for package in packages:
        plans.append([package.id, translate_regions(package.name, user_language)])

    # Сортировка по имени региона (по алфавиту)
    plans = sorted(plans, key=lambda x: x[1])

    return plans


# Региональные eSIM: конкретный регион -> тарифы
async def esim_regional_selected_region_plans(region_id):
    plans = []

    packages = await DataBase_RegionalTariff.filter(region=region_id).all()

    for package in packages:
        plans.append([package.id, format_number(package.gb), package.days, format_number(package.price)])

    # Сортировка: по объему, затем по количеству дней, затем по цене
    plans.sort(key=lambda x: (x[1], x[2], x[3]))

    return plans


# Региональные eSIM: Конкретный регион -> страны региона (текст при выборе конкретного тарифа)
async def esim_regional_countries(plan_id, region_id, user_language):
    countries = await DataBase_RegionalCountry.filter(tariff=plan_id, region=region_id).all()

    countries.sort(key=lambda x: x.location_name)

    countries_text_parts = [
        f"{code_to_flag(i.location_code)} {translate_countries(i.location_name, user_language)}"
        for i in countries
    ]

    return ", ".join(countries_text_parts)


# Международные eSIM: тарифы
async def esim_global():
    plans = []

    packages = await DataBase_EsimPackageGlobal.all()

    for package in packages:
        plans.append([package.id, format_number(package.gb), package.days, format_number(package.price)])

    # Сортировка: по объему, затем по количеству дней, затем по цене
    plans.sort(key=lambda x: (x[1], x[2], x[3]))

    return plans


# Международные eSIM: поддерживаемые страны
async def esim_global_countries(plan_id, user_language):
    countries = await DataBase_EsimCountryGlobal.filter(package_id=plan_id).all()

    countries.sort(key=lambda x: x.location_name)

    countries_text_parts = [
        f"{code_to_flag(i.location_code)} {translate_countries(i.location_name, user_language)}"
        for i in countries
    ]

    return ", ".join(countries_text_parts)