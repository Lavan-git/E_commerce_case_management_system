from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.base import ApplicationError
from app.exceptions.case import (
    CaseNotFoundError,
    InvalidCaseResolutionError,
    InvalidCaseStatusTransitionError,
    InvalidCaseTypeError,
)


def application_exception_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
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

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.__class__.__name__,
                "message": str(exc),
            }
        },
    )