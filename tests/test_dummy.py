import typing as tp

import pytest

from unit_commitment.production_plan.calculate_production_plan import (
    calculate_production_plan,
)
from unit_commitment.production_plan.dummy import dummy_response

if tp.TYPE_CHECKING:
    from unit_commitment.pydantic_models import Payload


def test_dummy_response(payload: "Payload"):
    result = calculate_production_plan(payload, method="dummy")
    expected = dummy_response(payload)
    assert result == expected
