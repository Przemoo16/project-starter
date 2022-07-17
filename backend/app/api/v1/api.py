import fastapi

from app.api.v1.routers import auth, config, health, users

router = fastapi.APIRouter()
router.include_router(auth.router, prefix="/token", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(config.router, prefix="/config", tags=["config"])
router.include_router(health.router, prefix="/health", tags=["health"])
