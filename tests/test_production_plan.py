import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.pydantic_models import Payload
from production_plan.greedy import dummy_response

client = TestClient(app)


def test_production_plan(payload: Payload):
    # Convert the Pydantic object to a dictionary
    payload_dict = payload.model_dump_json()

    # Make the API call
    response = client.post("/productionplan", json=payload_dict)

    # Check the status code
    assert response.status_code == 200

    # Get the expected response using your dummy_response function
    expected_response = dummy_response(payload)

    # Convert the expected Pydantic objects to dictionaries
    expected_response_dict = [obj.model_dump_json() for obj in expected_response]

    # Check the response
    assert response.json() == expected_response_dict
