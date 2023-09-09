import typing as tp

import pytest

from unit_commitment.production_plan.greedy import calculate_production_plan

if tp.TYPE_CHECKING:
    from unit_commitment.pydantic_models import Payload, ResponsePowerPlant


def validate_greedy_output(output: list["ResponsePowerPlant"], payload: "Payload"):
    total_power = sum(plant["p"] for plant in output)
    assert total_power == payload.load  # Total power should match the load

    for plant in output:
        name = plant["name"]
        original_plant = next(p for p in payload.powerplants if p.name == name)
        assert plant["p"] >= original_plant.pmin  # Should be above pmin
        assert plant["p"] <= original_plant.pmax  # Should be below pmax


def test_greedy_algorithm(payload: "Payload"):
    result = calculate_production_plan(payload, method="greedy")
    validate_greedy_output(result, payload)
