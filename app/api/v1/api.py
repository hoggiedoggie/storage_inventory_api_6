from fastapi import APIRouter, Depends
from app.api.v1.endpoints import auth, storage, yandex_auth
from app.api.v1.deps import get_current_user

api_router = APIRouter()



api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

api_router.include_router(
    storage.router, 
    prefix="/devices", 
    tags=["Storage"],
    dependencies=[Depends(get_current_user)] 
)

api_router.include_router(yandex_auth.router, prefix="/yandex", tags=["Yandex OAuth"])