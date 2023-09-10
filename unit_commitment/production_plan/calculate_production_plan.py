import typing as tp

from unit_commitment.production_plan.dummy import dummy_response
from unit_commitment.production_plan.greedy import allocate_power

if tp.TYPE_CHECKING:
    from unit_commitment.pydantic_models import Payload, ResponsePowerPlant


def calculate_production_plan(
    payload: "Payload", method: str = "dummy"
) -> list["ResponsePowerPlant"]:
    if method == "dummy":
        return dummy_response(payload)
    elif method == "greedy":
        return allocate_power(payload.load, payload.fuels, payload.powerplants)
    else:
        raise ValueError("Invalid method specified")
