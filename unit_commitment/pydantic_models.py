import typing as tp

from pydantic import BaseModel, Field, field_validator


class Fuel(BaseModel):
    gas: float = Field(..., alias="gas(euro/MWh)")
    kerosine: float = Field(..., alias="kerosine(euro/MWh)")
    co2: float = Field(..., alias="co2(euro/ton)")
    wind: int = Field(..., alias="wind(%)")

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(
            **{
                "gas(euro/MWh)": kwargs.get("gas", 0),
                "kerosine(euro/MWh)": kwargs.get("kerosine", 0),
                "co2(euro/ton)": kwargs.get("co2", 0),
                "wind(%)": kwargs.get("wind", 0),
            }
        )

    @field_validator("gas")
    def validate_gas(cls, value):
        if value < 0:
            raise ValueError("Gas price must be non-negative")
        return value

    class ConfigDict:
        populate_by_name = True


class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int
    allowed_values: tp.ClassVar[list[str]] = ["gasfired", "turbojet", "windturbine"]

    @field_validator("type")
    def validate_type(cls, value):
        if value not in cls.allowed_values:
            raise ValueError(f"Plant types must be one of: {cls.allowed_values}")
        return value


class Payload(BaseModel):
    load: int
    fuels: Fuel
    powerplants: list[PowerPlant]


class ResponsePowerPlant(BaseModel):
    name: str
    p: float


class ResponsePowerPlantList(BaseModel):
    items: list[ResponsePowerPlant]
