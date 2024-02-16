from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.core.config import settings
from jose import jwt, JWTError
from app.db.engine import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user based on the provided token.

    Parameters:
    - token (str): The authentication token.

    Returns:
    - dict: The payload of the decoded token.

    Raises:
    - HTTPException: If the credentials cannot be validated.
    """
    if db.blocklist.find_one({"token": token}):
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload

    except JWTError as e:
        print(e)
        raise credentials_exception
