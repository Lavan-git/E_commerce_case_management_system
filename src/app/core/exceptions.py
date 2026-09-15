import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.base import ApplicationError
from app.exceptions.case import (
    CaseNotFoundError,
    InvalidCaseResolutionError,
    InvalidCaseStatusTransitionError,
    InvalidCaseTypeError,
)

logger = logging.getLogger("app.exceptions")


def application_exception_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    if isinstance(exc, CaseNotFoundError):
        status_code = 404

    elif isinstance(
        exc,
        (
            InvalidCaseTypeError,
            InvalidCaseResolutionError,
            InvalidCaseStatusTransitionError,
        ),
    ):
        status_code = 400

    else:
        status_code = 400

    logger.warning(
        "application.error",
        extra={
            "request_id": request_id,
            "status_code": status_code,
        },
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.__class__.__name__,
                "message": str(exc),
                "request_id": request_id,
            }
        },
    )