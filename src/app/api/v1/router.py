from fastapi import APIRouter

from app.api.v1 import cases, health


router = APIRouter(
    prefix="/api/v1",
)

router.include_router(
    health.router,
)

router.include_router(
    cases.router,
)