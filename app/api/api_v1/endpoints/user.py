from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from app.core.security import pwd_context, create_access_token, blacklist_token
from app.api.deps import oauth2_scheme
from app.db.engine import db


router = APIRouter()


@router.post(
    "/register",
    responses={
        200: {
            "description": "Successful Registration",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User registered successfully",
                        "user_id": "string",
                    }
                }
            },
        },
        500: {
            "description": "Failed to register user",
            "content": {
                "application/json": {"example": {"detail": "Failed to register user"}}
            },
        },
    },
)
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
) -> JSONResponse:
    """
    Register a new user.

    Args:
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        role (str): The role of the user.

    Returns:
        JSONResponse: A JSON response containing the message and user_id if the user is registered successfully.

    Raises:
        HTTPException: If failed to register the user.
    """
    user_dict = {
        "username": username,
        "email": email,
        "password": password,
        "role": role,
    }
    user_dict["password"] = pwd_context.hash(user_dict["password"])
    result = db.UserRegistration.insert_one(user_dict)
    if result.acknowledged:
        return JSONResponse(
            status_code=200,
            content={
                "message": "User registered successfully",
                "user_id": str(result.inserted_id),
            },
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to register user")


@router.post(
    "/login",
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


@router.get("/logout", response_model=None)
async def logout(token: str = Depends(oauth2_scheme)):
    """
    Log out a user.
    Invalidate the user's access token.

    Returns:
        JSONResponse: A JSON response indicating that the user has been logged out.

    TODO: Implement logout logic.
    """
    blacklist_token(token)
    print(token)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Logged out successfully",
        },
    )
