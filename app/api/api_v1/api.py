from fastapi import APIRouter
from app.api.api_v1.endpoints import company, developers, job, login

api_router = APIRouter()


api_router.include_router(login.router, tags=["login"])
api_router.include_router(company.router, prefix="/company", tags=["company"])
api_router.include_router(developers.router, prefix="/developers", tags=["developers"])
api_router.include_router(job.router, prefix="/job", tags=["job"])
