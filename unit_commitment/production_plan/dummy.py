from unit_commitment.pydantic_models import Payload, ResponsePowerPlant


def dummy_response(payload: "Payload") -> list[ResponsePowerPlant]:
    return [
        ResponsePowerPlant(name="windpark1", p=90.0),
        ResponsePowerPlant(name="windpark2", p=21.6),
        ResponsePowerPlant(name="gasfiredbig1", p=460.0),
        ResponsePowerPlant(name="gasfiredbig2", p=338.4),
        ResponsePowerPlant(name="gasfiredsomewhatsmaller", p=0.0),
        ResponsePowerPlant(name="tj1", p=0.0),
    ]
