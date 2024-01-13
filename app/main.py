from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings
from app.db.engine import check_db_connection
from app.api.api_v1.api import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get(
    "/",
    response_class=HTMLResponse,
    responses={404: {"description": "Not found"}, 200: {"description": "OK"}},
    tags=["root"],
)
def read_root():
    db_status = check_db_connection()
    print(db_status)
    return f"""<h1>Kerala Devs</h1>
    <p>API is working fine</p>
    <p>Database status: {db_status["status"]}</p>
"""


app.include_router(api_router, prefix=settings.API_V1_STR)
