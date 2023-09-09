import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.pydantic_models import (Payload, ResponsePowerPlant,
                                        ResponsePowerPlantList)
from production_plan.greedy import dummy_response

ROUTE_PREFIX = "/api/v1"
client = TestClient(app)


def test_production_plan(payload: Payload):
    # Convert the Pydantic object to a dictionary
    payload_dict = payload.model_dump(by_alias=True)

    # Make the API call
    response = client.post(f"{ROUTE_PREFIX}/productionplan", json=payload_dict)

    # Check the status code
    assert response.status_code == 200

    # Get the expected response using your dummy_response function
    expected_response = ResponsePowerPlantList(items=dummy_response(payload))
    response_plants = [ResponsePowerPlant(**plant) for plant in response.json()]
    # Initialize ResponsePowerPlantList
    response_list = ResponsePowerPlantList(items=response_plants)

    # Check the response
    assert expected_response == response_list
