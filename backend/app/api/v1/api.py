import fastapi

from app.api.v1.routers import me, users

router = fastapi.APIRouter()

router.include_router(me.router, prefix="/me", tags=["me"])
router.include_router(users.router, prefix="/users", tags=["users"])
