# Временно для отладки
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
#
from database.models.esim_global import DataBase_EsimPackageGlobal
from database.models.esim_regional import DataBase_Region, DataBase_RegionalCountry, DataBase_RegionalTariff

async def esim_global():
    plans = []

    packages = await DataBase_EsimPackageGlobal.all()

    for package in packages:
        plans.append([package.id, package.gb, package.days, package.price])

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
        plans.append([package.id, package.gb, package.days, package.price])

    # Сортировка: по объему, затем по количеству дней, затем по цене
    plans.sort(key=lambda x: (x[1], x[2], x[3]))

    return plans
