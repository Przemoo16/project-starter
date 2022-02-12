import fastapi

from app.api.v1.routers import token, users

router = fastapi.APIRouter()
router.include_router(token.router, prefix="/token", tags=["token"])
router.include_router(users.router, prefix="/users", tags=["users"])
