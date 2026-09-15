from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.v1.router import router
from app.core.config import get_settings
from app.core.exceptions import application_exception_handler
from app.core.logging import configure_logging
from app.core.middleware import request_logging_middleware
from app.core.validation import validation_exception_handler
from app.exceptions.base import ApplicationError


configure_logging()

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "E-commerce dispute resolution and "
        "case management API."
    ),
)

app.middleware("http")(
    request_logging_middleware
)

app.add_exception_handler(
    ApplicationError,
    application_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.include_router(router)