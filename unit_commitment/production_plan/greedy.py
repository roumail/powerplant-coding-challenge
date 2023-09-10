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


def round_to_nearest_tenth(n):
    return round(n * 10) / 10


def allocate_power(
    load: int, fuels: "Fuel", powerplants: list["PowerPlant"]
) -> list[ResponsePowerPlant]:
    plant_fuel_costs = {}
    for plant in powerplants:
        plant_fuel_costs[plant.name] = calculate_fuel_cost(plant, fuels)
    sorted_plants = sorted(powerplants, key=lambda x: plant_fuel_costs[x.name])

    allocated_power = {}
    remaining_load = load

    # First, allocate to plants with zero pmin and lowest cost
    for plant in sorted_plants:
        if plant.pmin == 0:
            power_to_allocate = min(plant.pmax, remaining_load)
            allocated_power[plant.name] = power_to_allocate
            remaining_load -= power_to_allocate
            if remaining_load <= 0:
                break

    # Allocate power based on sorted plants
    for plant in sorted_plants:
        # If the remaining load is already fulfilled, break
        if remaining_load <= 0:
            break

        # If the plant has a minimum power output requirement, check if it should be switched on
        if plant.pmin > 0 and remaining_load >= plant.pmin:
            allocated_power[plant.name] = plant.pmin
            remaining_load -= plant.pmin

        # If the plant is already in allocated_power, get the current allocation; otherwise, start from zero
        current_allocation = allocated_power.get(plant.name, 0)

        # Allocate additional power if needed
        additional_power = min(plant.pmax - current_allocation, remaining_load)
        # Round to multiple of 0.1
        additional_power = round_to_nearest_tenth(additional_power)
        allocated_power[plant.name] = current_allocation + additional_power
        remaining_load -= additional_power

    if remaining_load > 0:
        print("Warning: Not all demand could be met.")

    # Convert the allocated_power dictionary to a list of ResponsePowerPlant objects
    result = [ResponsePowerPlant(name=name, p=p) for name, p in allocated_power.items()]

    return result
