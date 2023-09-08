from fastapi import APIRouter, HTTPException, Query
from app.models.pydantic_models import ResponsePowerPlant, Payload
from production_plan.greedy import calculate_production_plan

router = APIRouter()


@router.post("/productionplan", response_model=list[ResponsePowerPlant])
async def production_plan(payload: Payload, method: str = Query("dummy")):
    try:
        result = calculate_production_plan(payload, method)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))