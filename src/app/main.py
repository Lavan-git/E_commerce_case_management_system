from fastapi import FastAPI

from app.api.v1.router import router
from app.core.config import get_settings
from app.core.exceptions import application_exception_handler
from app.exceptions.base import ApplicationError


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "E-commerce dispute resolution and "
        "case management API."
    ),
)

app.add_exception_handler(
    ApplicationError,
    application_exception_handler,
)

app.include_router(router)