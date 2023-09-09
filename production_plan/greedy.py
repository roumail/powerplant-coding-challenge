from app.models.pydantic_models import Payload, ResponsePowerPlant


def calculate_production_plan(
    payload: Payload, method: str = "dummy"
) -> list[ResponsePowerPlant]:
    if method == "dummy":
        return dummy_response(payload)
    elif method == "greedy":
        return allocate_power(payload.load, payload.fuels, payload.powerplants)
    else:
        raise ValueError("Invalid method specified")


def dummy_response(payload: Payload) -> list[ResponsePowerPlant]:
    return [
        ResponsePowerPlant(name="windpark1", p=90.0),
        ResponsePowerPlant(name="windpark2", p=21.6),
        ResponsePowerPlant(name="gasfiredbig1", p=460.0),
        ResponsePowerPlant(name="gasfiredbig2", p=338.4),
        ResponsePowerPlant(name="gasfiredsomewhatsmaller", p=0.0),
        ResponsePowerPlant(name="tj1", p=0.0),
    ]


def allocate_power(
    load: int, fuels: dict[str, float], powerplants: list[dict[str, float]]
) -> list[dict[str, float]]:
    # Step 1: Sort Power Plants by Cost
    for plant in powerplants:
        fuel_cost = fuels[plant["type"]]
        plant["cost_per_mwh"] = fuel_cost / plant["efficiency"]
    powerplants.sort(key=lambda x: x["cost_per_mwh"])

    # Initialize variables
    allocated_power = []
    remaining_load = load

    # Step 2: Fulfill Minimum Requirements
    for plant in powerplants:
        if plant["pmin"] > 0:
            allocated_power.append({"name": plant["name"], "p": plant["pmin"]})
            remaining_load -= plant["pmin"]

    # Step 3 and 4: Allocate Remaining Load and Iterate
    i = 0
    while remaining_load > 0 and i < len(powerplants):
        plant = powerplants[i]
        additional_power = min(plant["pmax"] - allocated_power[i]["p"], remaining_load)

        allocated_power[i]["p"] += additional_power
        remaining_load -= additional_power

        i += 1

    # Check if all demand is met
    if remaining_load > 0:
        print("Warning: Not all demand could be met.")

    return allocated_power
