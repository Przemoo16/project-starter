import fastapi

from app.api.v1.routers import token

router = fastapi.APIRouter()
router.include_router(token.router, prefix="/token", tags=["token"])
