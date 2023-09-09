from fastapi import FastAPI

from unit_commitment.api.routes.api import router as api_router
from unit_commitment.core.config import settings


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, debug=settings.DEBUG, version=settings.VERSION
    )
    application.include_router(api_router, prefix=settings.API_PREFIX)
    return application


app = get_application()
