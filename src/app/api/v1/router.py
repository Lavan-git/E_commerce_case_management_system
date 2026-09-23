from fastapi import APIRouter

from app.api.v1 import cases, health,rag



router = APIRouter(
    prefix="/api/v1",
)

router.include_router(
    health.router,
)

router.include_router(
    cases.router,
)

router.include_router(
    rag.router,
)