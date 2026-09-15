import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger("app.http")


async def request_logging_middleware(
    request: Request,
    call_next,
):
    request_id = request.headers.get(
        "X-Request-ID"
    ) or str(uuid.uuid4())

    request.state.request_id = request_id

    start = time.perf_counter()

    try:
        response = await call_next(request)

        duration_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        logger.info(
            "http.request",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

        response.headers["X-Request-ID"] = request_id

        return response

    except Exception:
        duration_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        logger.exception(
            "http.request.failed",
            extra={
                "request_id": request_id,
                "duration_ms": duration_ms,
            },
        )

        raise