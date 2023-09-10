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

    # Then, fulfill minimum requirements
    for plant in sorted_plants:
        if plant.pmin > 0:
            allocated_power[plant.name] = plant.pmin
            remaining_load -= plant.pmin

    # Finally, allocate remaining load
    for plant in sorted_plants:
        if remaining_load <= 0:
            break

        current_allocation = allocated_power.get(plant.name, 0)
        additional_power = min(plant.pmax - current_allocation, remaining_load)

        allocated_power[plant.name] = current_allocation + additional_power
        remaining_load -= additional_power

    if remaining_load > 0:
        print("Warning: Not all demand could be met.")

    # Convert the allocated_power dictionary to a list of ResponsePowerPlant objects
    result = [ResponsePowerPlant(name=name, p=p) for name, p in allocated_power.items()]

    return result
