import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger("app.validation")


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    logger.warning(
        "request.validation_failed",
        extra={
            "request_id": request_id,
            "status_code": 422,
        },
    )

    details = []

    for error in exc.errors():
        error_detail = {
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
        }

        if "input" in error:
            error_detail["input"] = error["input"]

        details.append(error_detail)

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed.",
                "details": details,
                "request_id": request_id,
            }
        },
    )