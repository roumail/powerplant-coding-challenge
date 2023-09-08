# conftest.py

import pytest
from app.models.pydantic_models import Payload, Fuel, PowerPlant


powerplant_dicts = [
    {
        "name": "gasfiredbig1",
        "type": "gasfired",
        "efficiency": 0.53,
        "pmin": 100,
        "pmax": 460,
    },
    {
        "name": "gasfiredbig2",
        "type": "gasfired",
        "efficiency": 0.53,
        "pmin": 100,
        "pmax": 460,
    },
    {
        "name": "gasfiredsomewhatsmaller",
        "type": "gasfired",
        "efficiency": 0.37,
        "pmin": 40,
        "pmax": 210,
    },
    {"name": "tj1", "type": "turbojet", "efficiency": 0.3, "pmin": 0, "pmax": 16},
    {
        "name": "windpark1",
        "type": "windturbine",
        "efficiency": 1,
        "pmin": 0,
        "pmax": 150,
    },
    {
        "name": "windpark2",
        "type": "windturbine",
        "efficiency": 1,
        "pmin": 0,
        "pmax": 36,
    },
]

payload_params = [
    {"load": 480, "fuels": Fuel(gas=13.4, kerosine=50.8, co2=20, wind=60)},
    {"load": 480, "fuels": Fuel(gas=13.4, kerosine=50.8, co2=20, wind=0)},
    {"load": 910, "fuels": Fuel(gas=13.4, kerosine=50.8, co2=20, wind=60)},
]


@pytest.fixture(params=payload_params)
def payload(request):
    return Payload(
        load=request.param["load"],
        fuels=request.param["fuels"],
        powerplants=[PowerPlant(**plant_dict) for plant_dict in powerplant_dicts],
    )
