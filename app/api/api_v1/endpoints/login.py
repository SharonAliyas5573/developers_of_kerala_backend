from fastapi import APIRouter, Form, HTTPException
from app.db.engine import db
from app.core.security import pwd_context, create_access_token
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post(
    "/login",
    tags=["login"],
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "string",
                        "token_type": "string",
                        "role": "string",
                        "username": "string",
                    }
                }
            },
        },
        400: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {"example": {"detail": "Invalid credentials"}}
            },
        },
    },
)
async def login(
    username_or_email: str = Form(...), password: str = Form(...)
) -> JSONResponse:
    """
    login a user.
    Generate an access token for the user based on their username or email and password.

    Args:
        username_or_email (str): The username or email of the user.
        password (str): The password of the user.

    Returns:
        JSONResponse: A JSON response containing the access token, token type, role, and username.

    Raises:
        HTTPException: If the provided credentials are invalid.
    """
    user = db.UserRegistration.find_one(
        {"$or": [{"username": username_or_email}, {"email": username_or_email}]}
    )
    if user and pwd_context.verify(password, user["password"]):
        token_data = {
            "sub": str(user["_id"]),
            "username": user["username"],
            "role": user.get("role", ""),
        }
        token = create_access_token(token_data)
        return JSONResponse(
            {
                "access_token": token,
                "token_type": "bearer",
                "role": user.get("role", ""),
                "username": user["username"],
            }
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")
