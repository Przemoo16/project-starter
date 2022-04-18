import fastapi

from app.api.v1.routers import config, token, users

router = fastapi.APIRouter()
router.include_router(token.router, prefix="/token", tags=["token"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(config.router, prefix="/config", tags=["config"])
