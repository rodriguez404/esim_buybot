
from database.models.esim_local import DataBase_LocalCountry, DataBase_LocalTariff
from database.models.esim_global import DataBase_EsimPackageGlobal
from database.models.esim_regional import DataBase_Region, DataBase_RegionalCountry, DataBase_RegionalTariff

from microservices.format_number_UI import format_number

async def esim_global():
    plans = []

    packages = await DataBase_EsimPackageGlobal.all()

    for package in packages:
        plans.append([package.id, format_number(package.gb), package.days, format_number(package.price)])

    # Сортировка: по объему, затем по количеству дней, затем по цене
    plans.sort(key=lambda x: (x[1], x[2], x[3]))

    return plans


async def esim_regional():
    plans = []

    packages = await DataBase_Region.all()

    for package in packages:
        plans.append([package.id, package.name])

    # Сортировка по имени региона (по алфавиту)
    plans = sorted(plans, key=lambda x: x[1])

    return plans

async def esim_regional_selected_region_plans(region_id):
    plans = []

    packages = await DataBase_RegionalTariff.filter(region=region_id).all()

    for package in packages:
        plans.append([package.id, format_number(package.gb), package.days, format_number(package.price)])

    # Сортировка: по объему, затем по количеству дней, затем по цене
    plans.sort(key=lambda x: (x[1], x[2], x[3]))

    return plans


async def esim_local_countries():
    countries_list = []

    countries = await DataBase_LocalCountry.all()

    for country in countries:
        countries_list.append([country.id, country.location_name, country.location_code])

    # Сортировка по названию страны (по алфавиту)
    countries_list = sorted(countries_list, key=lambda x: x[1])

    return countries_list

async def esim_local_selected_country_plans(country_id):
    plans = []

    packages = await DataBase_LocalTariff.filter(country=country_id).all()

    for package in packages:
        plans.append([package.id, format_number(package.gb), package.days, format_number(package.price)])

    # Сортировка: по объему, затем по количеству дней, затем по цене
    plans.sort(key=lambda x: (x[1], x[2], x[3]))

    return plans