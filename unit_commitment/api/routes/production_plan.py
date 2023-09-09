from fastapi import APIRouter, HTTPException, Query

from unit_commitment.production_plan.greedy import calculate_production_plan
from unit_commitment.pydantic_models import Payload, ResponsePowerPlant

router = APIRouter()


@router.post("/productionplan", response_model=list[ResponsePowerPlant])
async def production_plan(payload: Payload, method: str = Query("dummy")):
    try:
        result = calculate_production_plan(payload, method)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
