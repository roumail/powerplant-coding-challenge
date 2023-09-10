import typing as tp

from unit_commitment.pydantic_models import ResponsePowerPlant

if tp.TYPE_CHECKING:
    from unit_commitment.pydantic_models import Fuel, PowerPlant

PLANT_TO_FUEL_MAP = {"gasfired": "gas", "turbojet": "kerosine", "windturbine": "wind"}


def calculate_fuel_cost(plant: "PowerPlant", fuels: "Fuel"):
    fuel_type = PLANT_TO_FUEL_MAP.get(plant.type)
    fuel_cost = getattr(fuels, fuel_type, 0)

    if fuel_type == "wind":
        return 0  # Wind power is free

    return fuel_cost / plant.efficiency


# The power produced by each powerplant has to be a multiple of 0.1 Mw and
# the sum of the power produced by all the powerplants together should equal the load.
def allocate_power(
    load: int, fuels: "Fuel", powerplants: list["PowerPlant"]
) -> list[ResponsePowerPlant]:
    # Step 1: Sort Power Plants by Cost
    plant_fuel_costs = {}
    for plant in powerplants:
        plant_fuel_costs[plant.name] = calculate_fuel_cost(plant, fuels)
    sorted_plants = sorted(powerplants, key=lambda x: plant_fuel_costs[x.name])

    # Initialize variables
    allocated_power = []
    remaining_load = load

    # Step 2: Fulfill Minimum Requirements
    for plant in sorted_plants:
        if plant.pmin > 0:
            allocated_power.append(ResponsePowerPlant(name=plant.name, p=plant.pmin))
            remaining_load -= plant.pmin

    # Step 3 and 4: Allocate Remaining Load and Iterate
    i = 0
    while remaining_load > 0 and i < len(sorted_plants):
        plant = sorted_plants[i]
        additional_power = min(plant.pmax - allocated_power[i].p, remaining_load)
        allocated_power[i].p += additional_power
        remaining_load -= additional_power
        i += 1

    # Check if all demand is met
    if remaining_load > 0:
        print("Warning: Not all demand could be met.")

    return allocated_power
