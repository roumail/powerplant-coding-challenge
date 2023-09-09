import typing as tp

import pytest

from production_plan.greedy import calculate_production_plan, dummy_response

if tp.TYPE_CHECKING:
    from app.models.pydantic_models import Payload


def test_dummy_response(payload: "Payload"):
    result = calculate_production_plan(payload, method="dummy")
    expected = dummy_response(payload)
    assert result == expected
