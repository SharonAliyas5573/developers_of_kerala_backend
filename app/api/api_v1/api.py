from fastapi import APIRouter
from app.api.api_v1.endpoints import company, developers, job, user

api_router = APIRouter()


api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(company.router, prefix="/company", tags=["company"])
api_router.include_router(developers.router, prefix="/developers", tags=["developers"])
api_router.include_router(job.router, prefix="/job", tags=["job"])
