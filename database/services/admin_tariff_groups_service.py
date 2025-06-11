from database.models.admin_tariff_groups import TariffGroup

mock_json = {
    "group_1": {
        "tariff_prices": [0.46, 1.39, 1.42, 2.30, 4.20, 7.00],
        "countries": ["TR"],
        "name": "группа 1"
    },
    "group_2": {
        "tariff_prices": [0.70, 1.70, 1.80, 2.70, 4.70, 8.20],
        "countries": ["AU", "JP"],
        "name": "группа 2"
    }
}

async def update_admin_tariff_groups():
    for group_name, group_data in mock_json.items():
        countries: dict[str] = group_data.get("countries", "[]")
        tariff_prices: dict[float] = group_data.get("tariff_prices", "[1.0, 1.0, 1.0, 1.0, 1.0]")
        name: str = group_data.get("name", "Безымянная группа")
        await TariffGroup.create(countries=countries, tariff_prices=tariff_prices, name=name)
