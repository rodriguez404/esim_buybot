# Временно для отладки
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
#
from database.models.esim_global import DataBase_EsimPackageGlobal

import re
from api.esim_access import fetch, url_packagelist


# фетч по !GL, на выходе массив тарифов [ [name, price, currency], ... ]
async def esim_global1():
    data = await fetch(url_packagelist, payload={'locationCode': '!GL'})
    plans = []
    package_list: dict = data.get('obj', {}).get('packageList', [])

    for package in package_list:
        name = package.get("name", "")
        price = str(int(package.get("price", 0)) // 10000) + "$"
        # currency = package.get("currencyCode", []) # Если нужно брать вид валюты, но там вроде всё только в долларах

        name = str(name).split()                               # ['Global138 1GB 30Days'] -> ['Global138', '1GB', '30Days']
        gb_amount = re.search(r'\d+', name[-2]).group() # ['Global138', '1GB', '30Days'] -> ['Global138', '1', '30Days']
        duration = re.search(r'\d+', name[-1]).group()  # ['Global138', '1GB', '30Days'] -> ['Global138', '1', '30']
        name = f"{gb_amount} ГБ на {duration} дней"            # ['Global138', '1GB', '30'] -> ['1GB на 30 дней']

        plans.append([name, price])

    plans = sorted(plans, key=lambda x: x[1])                  # Сортировка по цене, сначала дешевые
    return plans


async def esim_global():
    plans = []

    packages = await DataBase_EsimPackageGlobal.all()

    for package in packages:
        plans.append([package.id, package.gb, package.days, package.price])

    # Сортировка: по объему, затем по количеству дней, затем по цене
    plans.sort(key=lambda x: (x[1], x[2], x[3]))

    return plans


# фетч по !RL, на выходе массив тарифов [ [name, price, currency], ... ]
async def esim_regional():
    data = await fetch(url_packagelist, payload={'locationCode': '!RG'})
    plans = []
    package_list: dict = data.get('obj', {}).get('packageList', [])

    for package in package_list:
        name = package.get("name", "")
        name = str(name).split()
        if name and name[0] not in plans:
            plans.append(name[0])

    plans = sorted(plans)                                       # Сортировка регионов по алфавиту
    return plans