from fastapi import FastAPI

from app.api.routes.api import router as api_router
from app.core.config import settings


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, debug=settings.DEBUG, version=settings.VERSION
    )
    application.include_router(api_router, prefix=settings.API_PREFIX)
    return application


app = get_application()
