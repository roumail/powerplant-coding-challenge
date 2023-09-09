from pydantic import BaseModel, Field, validator


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

    @validator("gas")
    def validate_gas(cls, value):
        if value < 0:
            raise ValueError("Gas price must be non-negative")
        return value

    class Config:
        allow_population_by_field_name = True


class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int


class Payload(BaseModel):
    load: int
    fuels: Fuel
    powerplants: list[PowerPlant]


class ResponsePowerPlant(BaseModel):
    name: str
    p: float
