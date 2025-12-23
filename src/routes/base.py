from fastapi import APIRouter

base_router = APIRouter(
    prefix="/api/v1",
    tags=["health_check"]
)


@base_router.get("/health_check")
async def health_check():

    return {
        "status": "ok"
    }
