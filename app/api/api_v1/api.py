from fastapi import APIRouter, Security
from app.api.api_v1.endpoints import company, developers, job, user
from app.api.deps import get_current_user

api_router = APIRouter()


api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(
    company.router,
    prefix="/company",
    tags=["company"],
    dependencies=[Security(get_current_user)],
)
api_router.include_router(
    developers.router,
    prefix="/developers",
    tags=["developers"],
    dependencies=[Security(get_current_user)],
)
api_router.include_router(
    job.router, prefix="/job", tags=["job"], dependencies=[Security(get_current_user)]
)
