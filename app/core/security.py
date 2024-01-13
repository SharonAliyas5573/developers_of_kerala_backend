from datetime import datetime, timedelta


from jose import jwt
from passlib.context import CryptContext

from fastapi import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.engine import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = settings.ALGORITHM
ACESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY


def create_access_token(data: dict):
    """
    Create an access token using the provided data.

    Args:
        data (dict): The data to be encoded in the access token.

    Returns:
        str: The encoded access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def delete_blocklisted_tokens():
    current_time = datetime.utcnow()
    db.blocklist.delete_many({"expire": {"$lt": current_time}})


def blacklist_token(token: str, background_tasks: BackgroundTasks = None):
    # Decode the token and get the expiry time
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expire = payload.get("exp")
    db.blocklist.insert_one({"token": token, "expire": expire})

    if background_tasks is not None:
        background_tasks.add_task(delete_blocklisted_tokens)
