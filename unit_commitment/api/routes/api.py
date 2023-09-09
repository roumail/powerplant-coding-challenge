from fastapi import APIRouter

from unit_commitment.api.routes import production_plan

router = APIRouter()
router.include_router(production_plan.router, tags=["production_plan"])
